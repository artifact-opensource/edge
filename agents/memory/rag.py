"""
Hybrid RAG Engine
=================

Combines FTS5 keyword search (BM25 scoring) with neural embedding
similarity search, merged via Reciprocal Rank Fusion (RRF).

This replaces the documentation-only RAG with a real implementation
that sits on top of the existing ``enterprise_db.py`` FTS5 engine
and the new ``EmbeddingStore``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from agents.config import EmbeddingConfig, RAGConfig
from agents.memory.embeddings import EmbeddingStore, _content_hash
from agents.providers.base import EmbeddingProvider

# We import the existing enterprise DB engine
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from database.enterprise_db import EnterpriseDB

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """A single search result with combined scoring."""

    document_id: str
    title: str = ""
    content: str = ""
    file_path: str = ""
    category: str = ""
    score: float = 0.0
    keyword_rank: int | None = None
    semantic_rank: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class HybridRAG:
    """Hybrid search engine: FTS5 BM25 + neural embeddings + RRF.

    Workflow:
      1. Run FTS5 keyword search → ranked list by BM25
      2. Embed the query → cosine similarity against stored embeddings
      3. Reciprocal Rank Fusion merges both lists
      4. Return top-k with combined scores

    This is the real RAG that replaces ``RAG-USAGE-GUIDE.md`` documentation.
    """

    def __init__(
        self,
        db: EnterpriseDB,
        embedding_store: EmbeddingStore,
        embedding_provider: EmbeddingProvider,
        config: RAGConfig | None = None,
    ):
        self.db = db
        self.embedding_store = embedding_store
        self.embedding_provider = embedding_provider
        self.config = config or RAGConfig()

    async def search(
        self,
        query: str,
        limit: int | None = None,
        scope: list[str] | None = None,
    ) -> list[SearchResult]:
        """Run hybrid search combining keyword and semantic results.

        Args:
            query: Natural language search query.
            limit: Max results to return.
            scope: Optional list of categories to filter by.

        Returns:
            List of SearchResult sorted by combined relevance.
        """
        limit = limit or self.config.default_limit
        search_limit = limit * 3  # Over-fetch for better RRF merging

        # 1. FTS5 keyword search
        keyword_results = self._keyword_search(query, search_limit, scope)

        # 2. Neural embedding search
        semantic_results = await self._semantic_search(query, search_limit)

        # 3. Reciprocal Rank Fusion
        merged = self._reciprocal_rank_fusion(
            keyword_results, semantic_results, limit
        )

        return merged

    async def search_keyword_only(
        self, query: str, limit: int = 10, scope: list[str] | None = None
    ) -> list[SearchResult]:
        """FTS5-only search (no embedding provider needed)."""
        return self._keyword_search(query, limit, scope)

    async def search_semantic_only(
        self, query: str, limit: int = 10
    ) -> list[SearchResult]:
        """Embedding-only search."""
        return await self._semantic_search(query, limit)

    # ── Embedding Index Management ───────────────────────────────────────

    async def index_documents(self, batch_size: int = 64) -> dict[str, int]:
        """Embed all documents in the enterprise DB and store vectors.

        Skips documents that already have up-to-date embeddings.
        Returns stats: {indexed, skipped, errors}.
        """
        docs = self.db.query("SELECT id, title, content, category, file_path FROM documents")
        stats = {"indexed": 0, "skipped": 0, "errors": 0}

        batch_texts: list[str] = []
        batch_docs: list[dict] = []

        for doc in docs:
            text = self._build_document_text(doc)
            chash = _content_hash(text)

            if self.embedding_store.has_embedding(doc["id"], chash):
                stats["skipped"] += 1
                continue

            batch_texts.append(text)
            batch_docs.append({**doc, "_content_hash": chash})

            if len(batch_texts) >= batch_size:
                indexed, errors = await self._embed_and_store_batch(
                    batch_texts, batch_docs
                )
                stats["indexed"] += indexed
                stats["errors"] += errors
                batch_texts.clear()
                batch_docs.clear()

        # Process remaining
        if batch_texts:
            indexed, errors = await self._embed_and_store_batch(
                batch_texts, batch_docs
            )
            stats["indexed"] += indexed
            stats["errors"] += errors

        logger.info(
            "Indexing complete: %d indexed, %d skipped, %d errors",
            stats["indexed"],
            stats["skipped"],
            stats["errors"],
        )
        return stats

    # ── Private Methods ──────────────────────────────────────────────────

    def _keyword_search(
        self, query: str, limit: int, scope: list[str] | None = None
    ) -> list[SearchResult]:
        """Run FTS5 keyword search via the existing enterprise DB."""
        try:
            rows = self.db.search(query, limit=limit)
        except Exception as exc:
            logger.warning("FTS5 search failed for query '%s': %s", query, exc)
            return []

        results = []
        for rank, row in enumerate(rows):
            if scope and row.get("category") not in scope:
                continue
            results.append(
                SearchResult(
                    document_id=row.get("id", ""),
                    title=row.get("title", ""),
                    content=(row.get("content", "") or "")[:500],
                    file_path=row.get("file_path", ""),
                    category=row.get("category", ""),
                    score=abs(row.get("relevance_score", 0)),
                    keyword_rank=rank,
                )
            )
        return results

    async def _semantic_search(
        self, query: str, limit: int
    ) -> list[SearchResult]:
        """Embed query and search stored vectors."""
        try:
            query_embeddings = await self.embedding_provider.embed([query])
            if not query_embeddings or not query_embeddings[0]:
                return []
        except Exception as exc:
            logger.warning("Embedding generation failed: %s", exc)
            return []

        results_raw = self.embedding_store.cosine_search(
            query_embeddings[0], limit=limit
        )

        # Hydrate results with document metadata
        results = []
        for rank, (doc_id, score) in enumerate(results_raw):
            doc = self.db.get_by_id("documents", doc_id)
            if doc:
                results.append(
                    SearchResult(
                        document_id=doc_id,
                        title=doc.get("title", ""),
                        content=(doc.get("content", "") or "")[:500],
                        file_path=doc.get("file_path", ""),
                        category=doc.get("category", ""),
                        score=score,
                        semantic_rank=rank,
                    )
                )
        return results

    def _reciprocal_rank_fusion(
        self,
        keyword_results: list[SearchResult],
        semantic_results: list[SearchResult],
        limit: int,
    ) -> list[SearchResult]:
        """Merge keyword and semantic results using RRF.

        RRF score = sum(1 / (k + rank)) across both result lists.
        This is provably better than linear score combination because
        it's rank-based and invariant to score scale differences.
        """
        k = self.config.rrf_k
        scores: dict[str, float] = {}
        result_map: dict[str, SearchResult] = {}

        for rank, result in enumerate(keyword_results):
            doc_id = result.document_id
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
            if doc_id not in result_map:
                result_map[doc_id] = result

        for rank, result in enumerate(semantic_results):
            doc_id = result.document_id
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
            if doc_id not in result_map:
                result_map[doc_id] = result
            else:
                # Merge rank info
                result_map[doc_id].semantic_rank = result.semantic_rank

        # Sort by RRF score descending
        sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        results = []
        for doc_id in sorted_ids[:limit]:
            result = result_map[doc_id]
            result.score = scores[doc_id]
            results.append(result)

        return results

    async def _embed_and_store_batch(
        self, texts: list[str], docs: list[dict]
    ) -> tuple[int, int]:
        """Embed a batch of texts and store them."""
        indexed = 0
        errors = 0
        try:
            embeddings = await self.embedding_provider.embed(texts)
            records = []
            for doc, emb in zip(docs, embeddings):
                records.append(
                    {
                        "document_id": doc["id"],
                        "embedding": emb,
                        "model": self.embedding_provider.name,
                        "chunk_index": 0,
                        "content_hash": doc.get("_content_hash", ""),
                    }
                )
            indexed = self.embedding_store.store_batch(records)
        except Exception as exc:
            logger.error("Batch embedding failed: %s", exc)
            errors = len(texts)
        return indexed, errors

    @staticmethod
    def _build_document_text(doc: dict) -> str:
        """Build a text representation of a document for embedding."""
        parts = []
        if doc.get("title"):
            parts.append(doc["title"])
        if doc.get("category"):
            parts.append(f"Category: {doc['category']}")
        if doc.get("content"):
            parts.append(doc["content"][:2000])
        elif doc.get("file_path"):
            parts.append(f"File: {doc['file_path']}")
        return "\n".join(parts)
