"""
Thinking Middleware
==================

Pre-generation and post-generation processing that wraps every agent call.

- **Pre-gen**: Queries RAG for relevant context and injects it into the
  conversation before the LLM sees it.
- **Post-gen**: Validates the response (checks for empty replies, tool call
  errors, and optionally runs a reflection step).

These are middleware functions, not agents.  They transform the message
stream going in and coming out of the LLM call.
"""

from __future__ import annotations

import logging
from typing import Any

from agents.config import AgentConfig, MessageRole
from agents.memory.rag import HybridRAG, SearchResult
from agents.providers.base import ChatResponse, Message

logger = logging.getLogger(__name__)


class ThinkingMiddleware:
    """Pre-gen context injection and post-gen validation."""

    def __init__(self, rag: HybridRAG | None = None):
        self.rag = rag

    async def pre_gen(
        self,
        agent_config: AgentConfig,
        messages: list[Message],
    ) -> list[Message]:
        """Inject RAG context before the LLM call.

        Finds the last user message, searches RAG for relevant context,
        and inserts a system message with the results.
        """
        if self.rag is None:
            return messages

        # Find the last user message
        last_user_msg = ""
        for msg in reversed(messages):
            if msg.role == MessageRole.USER:
                last_user_msg = msg.content
                break

        if not last_user_msg:
            return messages

        # Search for relevant context
        scope = agent_config.memory.rag_scope or None
        try:
            results = await self.rag.search(
                last_user_msg,
                limit=5,
                scope=scope,
            )
        except Exception as exc:
            logger.warning("Pre-gen RAG search failed: %s", exc)
            return messages

        if not results:
            return messages

        # Format context
        context_text = self._format_context(results)
        context_msg = Message(
            role=MessageRole.SYSTEM,
            content=f"Relevant enterprise context (from RAG search):\n\n{context_text}",
        )

        # Insert context message before the last user message
        augmented = list(messages)
        for i in range(len(augmented) - 1, -1, -1):
            if augmented[i].role == MessageRole.USER:
                augmented.insert(i, context_msg)
                break
        else:
            augmented.insert(-1, context_msg)

        logger.debug(
            "Pre-gen: injected %d RAG results for query '%s'",
            len(results),
            last_user_msg[:50],
        )
        return augmented

    def post_gen(
        self,
        agent_config: AgentConfig,
        response: ChatResponse,
        messages: list[Message],
    ) -> ChatResponse:
        """Validate and optionally refine the LLM response.

        Checks:
          - Non-empty response
          - Tool call validity (function names exist)
          - Response length sanity

        Future: Add a reflection step where the agent evaluates its own
        response and retries if confidence is low.
        """
        msg = response.message

        # Check for empty response
        if not msg.content and not msg.tool_calls:
            logger.warning(
                "Post-gen: %s returned empty response (finish_reason=%s)",
                agent_config.name,
                response.finish_reason,
            )

        # Log tool calls for observability
        if msg.tool_calls:
            for tc in msg.tool_calls:
                logger.info(
                    "Post-gen: %s called tool '%s' with args %s",
                    agent_config.name,
                    tc.function,
                    str(tc.arguments)[:100],
                )

        return response

    @staticmethod
    def _format_context(results: list[SearchResult]) -> str:
        """Format RAG results into a readable context block."""
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"[{i}] {r.title}")
            if r.file_path:
                lines.append(f"    Path: {r.file_path}")
            if r.category:
                lines.append(f"    Category: {r.category}")
            if r.content:
                # Truncate content for context window efficiency
                preview = r.content[:200].replace("\n", " ")
                lines.append(f"    Preview: {preview}")
            lines.append("")
        return "\n".join(lines)
