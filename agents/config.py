"""
Configuration Models
====================

Pydantic v2 models for every configuration surface in the agent system.
All validation happens here; downstream code trusts these objects.
"""

from __future__ import annotations

import enum
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


# ── Enums ────────────────────────────────────────────────────────────────────


class ProviderKind(str, enum.Enum):
    OLLAMA = "ollama"
    OPENAI_COMPAT = "openai_compat"


class NodeType(str, enum.Enum):
    AGENT = "agent"
    PYTHON = "python"
    HUMAN = "human"
    CONDITIONAL = "conditional"


class MessageRole(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


# ── Provider Configs ─────────────────────────────────────────────────────────


class ProviderConfig(BaseModel):
    """Base configuration for an LLM provider."""

    kind: ProviderKind
    base_url: str
    model: str
    api_key: str = ""
    timeout: float = 120.0
    max_retries: int = 3
    temperature: float = 0.7
    max_tokens: int = 4096


class OllamaConfig(ProviderConfig):
    kind: ProviderKind = ProviderKind.OLLAMA
    base_url: str = "http://localhost:11434"
    model: str = "llama3.2"
    embedding_model: str = "nomic-embed-text"


class OpenAICompatConfig(ProviderConfig):
    kind: ProviderKind = ProviderKind.OPENAI_COMPAT
    base_url: str = "http://localhost:1234/v1"
    model: str = "default"
    embedding_model: str = "text-embedding-3-small"


# ── Embedding Config ─────────────────────────────────────────────────────────


class EmbeddingConfig(BaseModel):
    """Configuration for the embedding subsystem."""

    provider: ProviderKind = ProviderKind.OLLAMA
    base_url: str = "http://localhost:11434"
    model: str = "nomic-embed-text"
    dimension: int = 768  # nomic-embed-text default
    api_key: str = ""
    batch_size: int = 64


# ── RAG Config ───────────────────────────────────────────────────────────────


class RAGConfig(BaseModel):
    """Hybrid RAG search configuration."""

    keyword_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    semantic_weight: float = Field(default=0.7, ge=0.0, le=1.0)
    rrf_k: int = Field(default=60, gt=0)
    default_limit: int = Field(default=5, gt=0)


# ── Memory Config ────────────────────────────────────────────────────────────


class MemoryConfig(BaseModel):
    """Per-agent memory scope."""

    rag_scope: list[str] = Field(default_factory=list)
    conversation_buffer: int = Field(default=20, gt=0)


# ── Tool Definition ──────────────────────────────────────────────────────────


class ToolSpec(BaseModel):
    """JSON-schema-compatible tool specification for LLM function calling."""

    name: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)


# ── Agent Config ─────────────────────────────────────────────────────────────


class DelegationConfig(BaseModel):
    """Who this agent can delegate to."""

    can_delegate_to: list[str] = Field(default_factory=list)


class AgentConfig(BaseModel):
    """Full configuration for a single agent."""

    name: str
    title: str = ""
    department: str = ""
    system_prompt: str
    provider_preference: list[str] = Field(
        default_factory=lambda: ["ollama/llama3.2"]
    )
    tools: list[str] = Field(default_factory=list)
    memory: MemoryConfig = Field(default_factory=MemoryConfig)
    delegation: DelegationConfig = Field(default_factory=DelegationConfig)
    temperature: float = 0.7
    max_tokens: int = 4096


# ── Workflow Configs ─────────────────────────────────────────────────────────


class WorkflowNodeConfig(BaseModel):
    """A single node in a workflow DAG."""

    id: str
    name: str
    type: NodeType = NodeType.PYTHON
    enabled: bool = True
    depends_on: list[str] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)
    # For agent nodes
    agent: str = ""
    prompt_template: str = ""
    # For python nodes
    function: str = ""
    # For human nodes
    approvers: list[str] = Field(default_factory=list)
    sla_hours: float = 0
    # For conditional nodes
    condition: str = ""
    true_branch: str = ""
    false_branch: str = ""


class WorkflowConfig(BaseModel):
    """A complete workflow definition."""

    id: str
    name: str
    description: str = ""
    department: str = ""
    type: str = ""
    enabled: bool = False
    schedule: str = ""
    nodes: list[WorkflowNodeConfig] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


# ── Runtime Config ───────────────────────────────────────────────────────────


class RuntimeConfig(BaseModel):
    """Top-level runtime configuration."""

    providers: list[ProviderConfig] = Field(default_factory=list)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    rag: RAGConfig = Field(default_factory=RAGConfig)
    db_path: Path = Path("database/data/enterprise.db")
    agents_dir: Path = Path("agents/configs")
    workflows_dir: Path = Path("enterprise/workflows")
    log_level: str = "INFO"
