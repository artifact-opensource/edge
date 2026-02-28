"""
Embedding Store
===============

SQLite-backed vector storage with numpy cosine similarity search.
Designed for the enterprise's ~490 documents where brute-force exact
nearest-neighbor is faster than any approximate index.

When scale demands it (100K+ documents), swap this backend for Hektor
(the company's own C++ HNSW vector database) with zero interface changes.
"""

from __future__ import annotations

import hashlib
import logging
import sqlite3
import struct
from pathlib import Path
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

# ── Schema ───────────────────────────────────────────────────────────────────

EMBEDDINGS_SCHEMA = """
CREATE TABLE IF NOT EXISTS embeddings (
    id            TEXT PRIMARY KEY,
    document_id   TEXT NOT NULL,
    chunk_index   INTEGER DEFAULT 0,
    embedding     BLOB NOT NULL,
    model         TEXT NOT NULL,
    dimension     INTEGER NOT NULL,
    content_hash  TEXT,
    created_at    TEXT DEFAULT (datetime('now')),
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_embeddings_document ON embeddings(document_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_model ON embeddings(model);
"""


def _serialize_vector(vec: list[float] | np.ndarray) -> bytes:
    """Pack a float vector into a compact binary blob."""
    arr = np.asarray(vec, dtype=np.float32)
    return arr.tobytes()


def _deserialize_vector(blob: bytes, dimension: int) -> np.ndarray:
    """Unpack a binary blob back into a numpy array."""
    return np.frombuffer(blob, dtype=np.float32, count=dimension)


def _content_hash(text: str) -> str:
    """SHA-256 hex digest of text content for change detection."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class EmbeddingStore:
    """SQLite-backed embedding storage with exact cosine similarity search.

    The store is intentionally simple: all embeddings are loaded into memory
    for search.  At 490 documents × 768 dimensions × 4 bytes = ~1.5 MB,
    this is trivially fast.

    For billion-scale, replace this class with a Hektor adapter that
    implements the same interface.
    """

    def __init__(self, db_path: Path | str):
        self.db_path = Path(db_path) if str(db_path) != ":memory:" else db_path
        if isinstance(self.db_path, Path):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: sqlite3.Connection | None = None
        self.initialize()

    @property
    def conn(self) -> sqlite3.Connection:
        if self._conn is None:
            db_str = str(self.db_path) if isinstance(self.db_path, Path) else self.db_path
            self._conn = sqlite3.connect(db_str)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL")
        return self._conn

    def initialize(self) -> None:
        """Create the embeddings table if it doesn't exist."""
        self.conn.executescript(EMBEDDINGS_SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── Write Operations ─────────────────────────────────────────────────

    def store(
        self,
        document_id: str,
        embedding: list[float] | np.ndarray,
        model: str,
        chunk_index: int = 0,
        content_hash: str = "",
    ) -> None:
        """Store an embedding vector for a document."""
        vec = np.asarray(embedding, dtype=np.float32)
        emb_id = f"{document_id}:{chunk_index}"
        self.conn.execute(
            """INSERT OR REPLACE INTO embeddings
               (id, document_id, chunk_index, embedding, model, dimension, content_hash)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                emb_id,
                document_id,
                chunk_index,
                _serialize_vector(vec),
                model,
                len(vec),
                content_hash,
            ),
        )
        self.conn.commit()

    def store_batch(
        self,
        records: list[dict[str, Any]],
    ) -> int:
        """Batch store embeddings.

        Each record: {document_id, embedding, model, chunk_index?, content_hash?}
        Returns number of records stored.
        """
        count = 0
        with self.conn:
            for rec in records:
                doc_id = rec["document_id"]
                chunk_idx = rec.get("chunk_index", 0)
                emb_id = f"{doc_id}:{chunk_idx}"
                vec = np.asarray(rec["embedding"], dtype=np.float32)
                self.conn.execute(
                    """INSERT OR REPLACE INTO embeddings
                       (id, document_id, chunk_index, embedding, model, dimension, content_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        emb_id,
                        doc_id,
                        chunk_idx,
                        _serialize_vector(vec),
                        rec["model"],
                        len(vec),
                        rec.get("content_hash", ""),
                    ),
                )
                count += 1
        return count

    def delete(self, document_id: str) -> None:
        """Remove all embeddings for a document."""
        self.conn.execute(
            "DELETE FROM embeddings WHERE document_id = ?", (document_id,)
        )
        self.conn.commit()

    # ── Read Operations ──────────────────────────────────────────────────

    def get(self, document_id: str, chunk_index: int = 0) -> np.ndarray | None:
        """Retrieve a single embedding vector."""
        row = self.conn.execute(
            "SELECT embedding, dimension FROM embeddings WHERE id = ?",
            (f"{document_id}:{chunk_index}",),
        ).fetchone()
        if row is None:
            return None
        return _deserialize_vector(row["embedding"], row["dimension"])

    def has_embedding(self, document_id: str, content_hash: str = "") -> bool:
        """Check if a document already has an up-to-date embedding."""
        row = self.conn.execute(
            "SELECT content_hash FROM embeddings WHERE document_id = ? AND chunk_index = 0",
            (document_id,),
        ).fetchone()
        if row is None:
            return False
        if content_hash and row["content_hash"] != content_hash:
            return False
        return True

    def count(self) -> int:
        """Total number of stored embeddings."""
        row = self.conn.execute("SELECT COUNT(*) as cnt FROM embeddings").fetchone()
        return row["cnt"] if row else 0

    # ── Search ───────────────────────────────────────────────────────────

    def cosine_search(
        self,
        query_embedding: list[float] | np.ndarray,
        limit: int = 10,
        model_filter: str = "",
    ) -> list[tuple[str, float]]:
        """Exact cosine similarity search over all stored embeddings.

        Returns list of (document_id, similarity_score) sorted descending.
        """
        query = np.asarray(query_embedding, dtype=np.float32)
        query_norm = np.linalg.norm(query)
        if query_norm == 0:
            return []
        query_normalized = query / query_norm

        sql = "SELECT document_id, embedding, dimension FROM embeddings"
        params: list[Any] = []
        if model_filter:
            sql += " WHERE model = ?"
            params.append(model_filter)

        rows = self.conn.execute(sql, params).fetchall()
        if not rows:
            return []

        # Vectorized cosine similarity
        doc_ids = [row["document_id"] for row in rows]
        dim = rows[0]["dimension"]
        matrix = np.stack(
            [_deserialize_vector(row["embedding"], row["dimension"]) for row in rows]
        )

        norms = np.linalg.norm(matrix, axis=1)
        norms[norms == 0] = 1.0
        normalized = matrix / norms[:, np.newaxis]
        similarities = normalized @ query_normalized

        # Sort and return top-k
        indices = np.argsort(similarities)[::-1][:limit]
        # Deduplicate by document_id (keep highest score)
        seen: set[str] = set()
        results: list[tuple[str, float]] = []
        for idx in indices:
            doc_id = doc_ids[idx]
            if doc_id not in seen:
                seen.add(doc_id)
                results.append((doc_id, float(similarities[idx])))
        return results[:limit]

    # ── Stats ────────────────────────────────────────────────────────────

    def stats(self) -> dict[str, Any]:
        """Return store statistics."""
        total = self.count()
        models = self.conn.execute(
            "SELECT model, COUNT(*) as cnt FROM embeddings GROUP BY model"
        ).fetchall()
        return {
            "total_embeddings": total,
            "by_model": {row["model"]: row["cnt"] for row in models},
        }
