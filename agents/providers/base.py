"""
Provider Abstract Base Classes
===============================

Defines the contract that all LLM and embedding providers must implement.
Every provider must support health-checking, chat completion, and optionally
embedding generation.  The ``ProviderChain`` class wraps multiple providers
and implements automatic fallback.
"""

from __future__ import annotations

import abc
import logging
from dataclasses import dataclass, field
from typing import Any

from agents.config import MessageRole

logger = logging.getLogger(__name__)


# ── Message Types ────────────────────────────────────────────────────────────


@dataclass
class ToolCall:
    """A tool/function call requested by the model."""

    id: str
    function: str
    arguments: dict[str, Any]


@dataclass
class Message:
    """A single message in a conversation."""

    role: MessageRole
    content: str = ""
    name: str | None = None
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to provider-compatible dict."""
        d: dict[str, Any] = {"role": self.role.value, "content": self.content}
        if self.name:
            d["name"] = self.name
        if self.tool_calls:
            d["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function,
                        "arguments": (
                            tc.arguments
                            if isinstance(tc.arguments, str)
                            else __import__("json").dumps(tc.arguments)
                        ),
                    },
                }
                for tc in self.tool_calls
            ]
        if self.tool_call_id:
            d["tool_call_id"] = self.tool_call_id
        return d


@dataclass
class ChatResponse:
    """Response from a chat completion call."""

    message: Message
    model: str = ""
    finish_reason: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)


# ── Exceptions ───────────────────────────────────────────────────────────────


class ProviderError(Exception):
    """Raised when a provider call fails."""

    def __init__(self, provider: str, message: str):
        self.provider = provider
        super().__init__(f"[{provider}] {message}")


class AllProvidersFailedError(Exception):
    """Raised when every provider in a chain has failed."""

    def __init__(self, errors: list[tuple[str, Exception]]):
        self.errors = errors
        detail = "; ".join(f"{name}: {err}" for name, err in errors)
        super().__init__(f"All providers failed: {detail}")


# ── Abstract Base Classes ────────────────────────────────────────────────────


class ChatProvider(abc.ABC):
    """Abstract chat completion provider."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Human-readable provider name (e.g. 'ollama/llama3.2')."""

    @abc.abstractmethod
    async def chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        """Send messages and return a completion."""

    @abc.abstractmethod
    async def health_check(self) -> bool:
        """Return True if the provider is reachable and ready."""


class EmbeddingProvider(abc.ABC):
    """Abstract embedding provider."""

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Human-readable provider name."""

    @property
    @abc.abstractmethod
    def dimension(self) -> int:
        """Embedding vector dimension."""

    @abc.abstractmethod
    async def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a batch of texts."""

    @abc.abstractmethod
    async def health_check(self) -> bool:
        """Return True if the embedding service is reachable."""


# ── Provider Chain ───────────────────────────────────────────────────────────


class ProviderChain(ChatProvider):
    """Tries providers in order until one succeeds.

    Implements the Gemini → Ollama → Local fallback pattern documented
    in ``LLM_Fallback_Playbook.md``, but now as real, executable code.
    """

    def __init__(self, providers: list[ChatProvider]):
        if not providers:
            raise ValueError("ProviderChain requires at least one provider")
        self._providers = providers

    @property
    def name(self) -> str:
        return "chain/" + "+".join(p.name for p in self._providers)

    @property
    def providers(self) -> list[ChatProvider]:
        return list(self._providers)

    async def chat(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> ChatResponse:
        errors: list[tuple[str, Exception]] = []
        for provider in self._providers:
            try:
                healthy = await provider.health_check()
                if not healthy:
                    logger.warning("Provider %s is not healthy, skipping", provider.name)
                    errors.append((provider.name, ProviderError(provider.name, "health check failed")))
                    continue
                response = await provider.chat(messages, tools, **kwargs)
                logger.info("Provider %s returned response", provider.name)
                return response
            except Exception as exc:
                logger.warning("Provider %s failed: %s", provider.name, exc)
                errors.append((provider.name, exc))
                continue
        raise AllProvidersFailedError(errors)

    async def health_check(self) -> bool:
        """At least one provider must be healthy."""
        for provider in self._providers:
            try:
                if await provider.health_check():
                    return True
            except Exception:
                continue
        return False


class EmbeddingChain(EmbeddingProvider):
    """Tries embedding providers in order until one succeeds."""

    def __init__(self, providers: list[EmbeddingProvider]):
        if not providers:
            raise ValueError("EmbeddingChain requires at least one provider")
        self._providers = providers

    @property
    def name(self) -> str:
        return "embed_chain/" + "+".join(p.name for p in self._providers)

    @property
    def dimension(self) -> int:
        return self._providers[0].dimension

    async def embed(self, texts: list[str]) -> list[list[float]]:
        errors: list[tuple[str, Exception]] = []
        for provider in self._providers:
            try:
                if await provider.health_check():
                    return await provider.embed(texts)
            except Exception as exc:
                errors.append((provider.name, exc))
                continue
        raise AllProvidersFailedError(errors)

    async def health_check(self) -> bool:
        for provider in self._providers:
            try:
                if await provider.health_check():
                    return True
            except Exception:
                continue
        return False
