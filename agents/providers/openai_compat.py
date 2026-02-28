"""
OpenAI-Compatible Provider
==========================

Works with any server that implements the OpenAI Chat Completions API:
  - LM Studio
  - llama.cpp server (``--api-like-OAI``)
  - vLLM
  - text-generation-inference (TGI)
  - Groq, Together, OpenRouter, Fireworks (cloud)
  - OpenAI itself

Also supports the ``/v1/embeddings`` endpoint for embedding generation.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from agents.config import MessageRole, OpenAICompatConfig
from agents.providers.base import (
    ChatProvider,
    ChatResponse,
    EmbeddingProvider,
    Message,
    ProviderError,
    ToolCall,
)

logger = logging.getLogger(__name__)


class OpenAICompatChatProvider(ChatProvider):
    """OpenAI-compatible chat completion via /v1/chat/completions."""

    def __init__(self, config: OpenAICompatConfig | None = None):
        self._config = config or OpenAICompatConfig()
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._config.api_key:
            headers["Authorization"] = f"Bearer {self._config.api_key}"
        self._client = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
            headers=headers,
        )

    @property
    def name(self) -> str:
        return f"openai_compat/{self._config.model}"

    async def chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        payload: dict[str, Any] = {
            "model": kwargs.get("model", self._config.model),
            "messages": [m.to_dict() for m in messages],
            "temperature": kwargs.get("temperature", self._config.temperature),
            "max_tokens": kwargs.get("max_tokens", self._config.max_tokens),
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = kwargs.get("tool_choice", "auto")

        for attempt in range(1, self._config.max_retries + 1):
            try:
                resp = await self._client.post("/chat/completions", json=payload)
                resp.raise_for_status()
                data = resp.json()
                return self._parse_response(data)
            except httpx.HTTPStatusError as exc:
                logger.warning(
                    "OpenAI-compat HTTP %d on attempt %d/%d: %s",
                    exc.response.status_code,
                    attempt,
                    self._config.max_retries,
                    exc.response.text[:200],
                )
                if attempt == self._config.max_retries:
                    raise ProviderError(
                        self.name, f"HTTP {exc.response.status_code}"
                    ) from exc
            except httpx.ConnectError as exc:
                raise ProviderError(
                    self.name, "connection refused — is the server running?"
                ) from exc

        raise ProviderError(self.name, "exhausted retries")

    async def health_check(self) -> bool:
        try:
            resp = await self._client.get("/models")
            return resp.status_code == 200
        except Exception:
            return False

    def _parse_response(self, data: dict[str, Any]) -> ChatResponse:
        choices = data.get("choices", [{}])
        choice = choices[0] if choices else {}
        msg_data = choice.get("message", {})

        tool_calls = None
        if msg_data.get("tool_calls"):
            tool_calls = []
            for tc in msg_data["tool_calls"]:
                fn = tc.get("function", {})
                args = fn.get("arguments", "{}")
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {"raw": args}
                tool_calls.append(
                    ToolCall(
                        id=tc.get("id", ""),
                        function=fn.get("name", ""),
                        arguments=args,
                    )
                )

        message = Message(
            role=MessageRole.ASSISTANT,
            content=msg_data.get("content", "") or "",
            tool_calls=tool_calls,
        )

        usage_data = data.get("usage", {})
        return ChatResponse(
            message=message,
            model=data.get("model", self._config.model),
            finish_reason=choice.get("finish_reason", "stop"),
            usage={
                "prompt_tokens": usage_data.get("prompt_tokens", 0),
                "completion_tokens": usage_data.get("completion_tokens", 0),
            },
            raw=data,
        )

    async def close(self) -> None:
        await self._client.aclose()


class OpenAICompatEmbeddingProvider(EmbeddingProvider):
    """OpenAI-compatible embedding via /v1/embeddings."""

    def __init__(
        self, config: OpenAICompatConfig | None = None, dimension: int = 1536
    ):
        self._config = config or OpenAICompatConfig()
        self._dimension = dimension
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._config.api_key:
            headers["Authorization"] = f"Bearer {self._config.api_key}"
        self._client = httpx.AsyncClient(
            base_url=self._config.base_url,
            timeout=self._config.timeout,
            headers=headers,
        )

    @property
    def name(self) -> str:
        return f"openai_compat/{self._config.embedding_model}"

    @property
    def dimension(self) -> int:
        return self._dimension

    async def embed(self, texts: list[str]) -> list[list[float]]:
        payload = {
            "model": self._config.embedding_model,
            "input": texts,
        }
        try:
            resp = await self._client.post("/embeddings", json=payload)
            resp.raise_for_status()
            data = resp.json()
            embeddings = [item["embedding"] for item in data.get("data", [])]
            if embeddings and self._dimension != len(embeddings[0]):
                self._dimension = len(embeddings[0])
            return embeddings
        except httpx.ConnectError as exc:
            raise ProviderError(self.name, "connection refused") from exc
        except httpx.HTTPStatusError as exc:
            raise ProviderError(
                self.name, f"HTTP {exc.response.status_code}"
            ) from exc

    async def health_check(self) -> bool:
        try:
            resp = await self._client.get("/models")
            return resp.status_code == 200
        except Exception:
            return False

    async def close(self) -> None:
        await self._client.aclose()
