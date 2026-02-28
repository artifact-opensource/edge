"""
Ollama Provider
===============

Chat + Embedding provider backed by a local Ollama instance.
Default model: llama3.2 (chat), nomic-embed-text (embeddings).

Ollama API reference:
  - POST /api/chat        — streaming/non-streaming chat
  - POST /api/embeddings  — text embeddings (v0.4.0+)
  - GET  /api/tags        — list available models
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from agents.config import MessageRole, OllamaConfig
from agents.providers.base import (
    ChatProvider,
    ChatResponse,
    EmbeddingProvider,
    Message,
    ProviderError,
    ToolCall,
)

logger = logging.getLogger(__name__)


class OllamaChatProvider(ChatProvider):
    """Ollama chat completion via /api/chat."""

    def __init__(self, config: OllamaConfig | None = None):
        self._config = config or OllamaConfig()
        self._client = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
        )

    @property
    def name(self) -> str:
        return f"ollama/{self._config.model}"

    async def chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self._config.model),
            "messages": [m.to_dict() for m in messages],
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", self._config.temperature),
                "num_predict": kwargs.get("max_tokens", self._config.max_tokens),
            },
        }

        if tools:
            payload["tools"] = tools

        for attempt in range(1, self._config.max_retries + 1):
            try:
                resp = await self._client.post("/api/chat", json=payload)
                resp.raise_for_status()
                data = resp.json()
                return self._parse_response(data)
            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "Ollama HTTP %d on attempt %d/%d: %s",
                    exc.response.status_code,
                    attempt,
                    self._config.max_retries,
                    exc.response.text[:200],
                )
                if attempt == self._config.max_retries:
                    raise ProviderError(self.name, f"HTTP {exc.response.status_code}") from exc
            except httpx.ConnectError as exc:
                raise ProviderError(self.name, "connection refused — is Ollama running?") from exc

        raise ProviderError(self.name, "exhausted retries")

    async def health_check(self) -> bool:
        try:
            resp = await self._client.get("/api/tags")
            return resp.status_code == 200
        except Exception:
            return False

    def _parse_response(self, data: dict[str, Any]) -> ChatResponse:
        msg_data = data.get("message", {})
        tool_calls = None

        if msg_data.get("tool_calls"):
            tool_calls = []
            for i, tc in enumerate(msg_data["tool_calls"]):
                fn = tc.get("function", {})
                tool_calls.append(
                    ToolCall(
                        id=f"call_{i}",
                        function=fn.get("name", ""),
                        arguments=fn.get("arguments", {}),
                    )
                )

        message = Message(
            role=MessageRole.ASSISTANT,
            content=msg_data.get("content", ""),
            tool_calls=tool_calls,
        )

        return ChatResponse(
            message=message,
            model=data.get("model", self._config.model),
            finish_reason="tool_calls" if tool_calls else "stop",
            usage={
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
            },
            raw=data,
        )

    async def close(self) -> None:
        await self._client.aclose()


class OllamaEmbeddingProvider(EmbeddingProvider):
    """Ollama embedding via /api/embeddings (v0.4.0+) or /api/embed."""

    def __init__(self, config: OllamaConfig | None = None, dimension: int = 768):
        self._config = config or OllamaConfig()
        self._dimension = dimension
        self._client = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
        )

    @property
    def name(self) -> str:
        return f"ollama/{self._config.embedding_model}"

    @property
    def dimension(self) -> int:
        return self._dimension

    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts.

        Tries /api/embed (Ollama ≥0.4.0 batch endpoint) first,
        then falls back to /api/embeddings (single-text endpoint).
        """
        # Try batch endpoint first (Ollama ≥ 0.4.0)
        try:
            resp = await self._client.post(
                "/api/embed",
                json={"model": self._config.embedding_model, "input": texts},
            )
            if resp.status_code == 200:
                data = resp.json()
                embeddings = data.get("embeddings", [])
                if embeddings:
                    if self._dimension != len(embeddings[0]):
                        self._dimension = len(embeddings[0])
                    return embeddings
        except Exception:
            pass

        # Fallback: single-text endpoint
        results: list[list[float]] = []
        for text in texts:
            resp = await self._client.post(
                "/api/embeddings",
                json={"model": self._config.embedding_model, "prompt": text},
            )
            resp.raise_for_status()
            data = resp.json()
            embedding = data.get("embedding", [])
            if embedding and self._dimension != len(embedding):
                self._dimension = len(embedding)
            results.append(embedding)

        return results

    async def health_check(self) -> bool:
        try:
            resp = await self._client.get("/api/tags")
            return resp.status_code == 200
        except Exception:
            return False

    async def close(self) -> None:
        await self._client.aclose()
