"""
Provider Factory
================

Constructs provider instances from configuration and assembles fallback chains.
"""

from __future__ import annotations

import logging
from typing import Any

from agents.config import (
    EmbeddingConfig,
    OllamaConfig,
    OpenAICompatConfig,
    ProviderConfig,
    ProviderKind,
)
from agents.providers.base import (
    ChatProvider,
    EmbeddingChain,
    EmbeddingProvider,
    ProviderChain,
)
from agents.providers.ollama import OllamaChatProvider, OllamaEmbeddingProvider
from agents.providers.openai_compat import (
    OpenAICompatChatProvider,
    OpenAICompatEmbeddingProvider,
)

logger = logging.getLogger(__name__)


def build_chat_provider(config: ProviderConfig) -> ChatProvider:
    """Instantiate a single chat provider from config."""
    if config.kind == ProviderKind.OLLAMA:
        ollama_cfg = OllamaConfig(
            base_url=config.base_url,
            model=config.model,
            api_key=config.api_key,
            timeout=config.timeout,
            max_retries=config.max_retries,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
        return OllamaChatProvider(ollama_cfg)
    elif config.kind == ProviderKind.OPENAI_COMPAT:
        oai_cfg = OpenAICompatConfig(
            base_url=config.base_url,
            model=config.model,
            api_key=config.api_key,
            timeout=config.timeout,
            max_retries=config.max_retries,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
        return OpenAICompatChatProvider(oai_cfg)
    else:
        raise ValueError(f"Unknown provider kind: {config.kind}")


def build_chat_chain(configs: list[ProviderConfig]) -> ProviderChain:
    """Build a fallback chain of chat providers."""
    providers = [build_chat_provider(c) for c in configs]
    return ProviderChain(providers)


def build_embedding_provider(config: EmbeddingConfig) -> EmbeddingProvider:
    """Instantiate an embedding provider from config."""
    if config.provider == ProviderKind.OLLAMA:
        ollama_cfg = OllamaConfig(
            base_url=config.base_url,
            embedding_model=config.model,
            api_key=config.api_key,
        )
        return OllamaEmbeddingProvider(ollama_cfg, dimension=config.dimension)
    elif config.provider == ProviderKind.OPENAI_COMPAT:
        oai_cfg = OpenAICompatConfig(
            base_url=config.base_url,
            embedding_model=config.model,
            api_key=config.api_key,
        )
        return OpenAICompatEmbeddingProvider(oai_cfg, dimension=config.dimension)
    else:
        raise ValueError(f"Unknown embedding provider: {config.provider}")


def parse_provider_preference(pref: str) -> ProviderConfig:
    """Parse a provider preference string like 'ollama/llama3.2' or
    'openai_compat/gpt-4o@https://api.openai.com/v1'.

    Format: ``<kind>/<model>[@<base_url>][?key=<api_key>]``
    """
    # Split off API key if present
    api_key = ""
    if "?key=" in pref:
        pref, api_key = pref.rsplit("?key=", 1)

    # Split off base URL if present
    base_url = ""
    if "@" in pref:
        pref, base_url = pref.rsplit("@", 1)

    kind_str, _, model = pref.partition("/")
    if not model:
        model = kind_str
        kind_str = "ollama"

    try:
        kind = ProviderKind(kind_str)
    except ValueError:
        kind = ProviderKind.OLLAMA

    # Set sensible defaults for base_url
    if not base_url:
        if kind == ProviderKind.OLLAMA:
            base_url = "http://localhost:11434"
        else:
            base_url = "http://localhost:1234/v1"

    return ProviderConfig(kind=kind, base_url=base_url, model=model, api_key=api_key)


def build_chain_from_preferences(prefs: list[str]) -> ProviderChain:
    """Build a provider chain from agent config preference strings."""
    configs = [parse_provider_preference(p) for p in prefs]
    return build_chat_chain(configs)
