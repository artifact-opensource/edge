"""
Conversation Memory
===================

SQLite-backed conversation history for agents.  Each agent maintains
its own conversation buffer (configurable size).  The buffer is a
sliding window of the most recent messages — older messages are
persisted but not included in the LLM context.

This also provides session-level conversation tracking for the runtime.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agents.config import MessageRole
from agents.providers.base import Message

logger = logging.getLogger(__name__)

CONVERSATION_SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
    id            TEXT PRIMARY KEY,
    session_id    TEXT NOT NULL,
    agent_id      TEXT NOT NULL,
    role          TEXT NOT NULL,
    content       TEXT NOT NULL DEFAULT '',
    tool_calls    TEXT,          -- JSON serialized
    tool_call_id  TEXT,
    name          TEXT,
    created_at    TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conv_agent ON conversations(agent_id);
CREATE INDEX IF NOT EXISTS idx_conv_time ON conversations(created_at);

CREATE TABLE IF NOT EXISTS sessions (
    id            TEXT PRIMARY KEY,
    task          TEXT NOT NULL DEFAULT '',
    status        TEXT DEFAULT 'active',
    agent_ids     TEXT,          -- JSON array of agents involved
    created_at    TEXT DEFAULT (datetime('now')),
    updated_at    TEXT DEFAULT (datetime('now'))
);
"""


class ConversationMemory:
    """SQLite-backed conversation history."""

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
        self.conn.executescript(CONVERSATION_SCHEMA)
        self.conn.commit()

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    # ── Session Management ───────────────────────────────────────────────

    def create_session(self, task: str = "") -> str:
        """Create a new conversation session. Returns session_id."""
        session_id = str(uuid.uuid4())[:8]
        self.conn.execute(
            "INSERT INTO sessions (id, task) VALUES (?, ?)",
            (session_id, task),
        )
        self.conn.commit()
        return session_id

    def close_session(self, session_id: str) -> None:
        """Mark a session as completed."""
        self.conn.execute(
            "UPDATE sessions SET status = 'completed', updated_at = ? WHERE id = ?",
            (datetime.now(timezone.utc).isoformat(), session_id),
        )
        self.conn.commit()

    # ── Message Storage ──────────────────────────────────────────────────

    def add_message(
        self, session_id: str, agent_id: str, message: Message
    ) -> str:
        """Store a message and return its ID."""
        msg_id = str(uuid.uuid4())[:12]
        tool_calls_json = None
        if message.tool_calls:
            tool_calls_json = json.dumps(
                [
                    {"id": tc.id, "function": tc.function, "arguments": tc.arguments}
                    for tc in message.tool_calls
                ]
            )

        self.conn.execute(
            """INSERT INTO conversations
               (id, session_id, agent_id, role, content, tool_calls, tool_call_id, name)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                msg_id,
                session_id,
                agent_id,
                message.role.value,
                message.content,
                tool_calls_json,
                message.tool_call_id,
                message.name,
            ),
        )
        self.conn.commit()
        return msg_id

    def get_messages(
        self,
        session_id: str,
        agent_id: str = "",
        limit: int = 50,
    ) -> list[Message]:
        """Retrieve conversation history for an agent in a session.

        Returns the most recent ``limit`` messages in chronological order.
        """
        sql = "SELECT * FROM conversations WHERE session_id = ?"
        params: list[Any] = [session_id]
        if agent_id:
            sql += " AND agent_id = ?"
            params.append(agent_id)
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)

        rows = self.conn.execute(sql, params).fetchall()
        rows = list(reversed(rows))  # Chronological order

        messages = []
        for row in rows:
            tool_calls = None
            if row["tool_calls"]:
                try:
                    tc_data = json.loads(row["tool_calls"])
                    from agents.providers.base import ToolCall

                    tool_calls = [
                        ToolCall(
                            id=tc["id"],
                            function=tc["function"],
                            arguments=tc["arguments"],
                        )
                        for tc in tc_data
                    ]
                except (json.JSONDecodeError, KeyError):
                    pass

            messages.append(
                Message(
                    role=MessageRole(row["role"]),
                    content=row["content"],
                    tool_calls=tool_calls,
                    tool_call_id=row["tool_call_id"],
                    name=row["name"],
                )
            )
        return messages

    def get_buffer(
        self, session_id: str, agent_id: str, buffer_size: int = 20
    ) -> list[Message]:
        """Get the most recent messages for context window injection."""
        return self.get_messages(session_id, agent_id, limit=buffer_size)

    # ── Stats ────────────────────────────────────────────────────────────

    def session_count(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) as cnt FROM sessions").fetchone()
        return row["cnt"] if row else 0

    def message_count(self, session_id: str = "") -> int:
        if session_id:
            row = self.conn.execute(
                "SELECT COUNT(*) as cnt FROM conversations WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        else:
            row = self.conn.execute(
                "SELECT COUNT(*) as cnt FROM conversations"
            ).fetchone()
        return row["cnt"] if row else 0
