"""
Agent Runtime
=============

The top-level orchestrator.  Receives a task, has the CEO agent classify
and delegate it, then routes to the appropriate C-suite agent who
executes it with tools and returns results.

This is the outer loop:

  Task → CEO classifies → Routes to C-suite agent → Agent executes → Result

The CEO decides *who* handles a task. The C-suite agent decides *how*.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import yaml

from agents.agent import AgentExecutor
from agents.config import (
    AgentConfig,
    EmbeddingConfig,
    MemoryConfig,
    ProviderConfig,
    ProviderKind,
    RAGConfig,
    RuntimeConfig,
)
from agents.memory.conversation import ConversationMemory
from agents.memory.embeddings import EmbeddingStore
from agents.memory.rag import HybridRAG
from agents.providers import build_chain_from_preferences, build_embedding_provider
from agents.providers.base import ChatProvider, EmbeddingProvider, Message
from agents.config import MessageRole
from agents.thinking import ThinkingMiddleware
from agents.tools import ToolRegistry
from agents.tools.enterprise import set_shared_resources

logger = logging.getLogger(__name__)

# Ensure enterprise modules are importable
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


class AgentRuntime:
    """Multi-agent runtime with CEO delegation pattern.

    The CEO agent receives all tasks and decides which C-suite agent
    should handle them.  Each C-suite agent has:
      - A specialized system prompt defining their role
      - A set of allowed tools
      - A scoped view of the RAG knowledge base
      - A conversation buffer for session continuity

    Usage::

        runtime = AgentRuntime.from_config()
        result = await runtime.process("What is our GRC compliance status?")
    """

    def __init__(
        self,
        agents: dict[str, AgentConfig],
        provider_chain: ChatProvider,
        rag: HybridRAG | None,
        tool_registry: ToolRegistry,
        thinking: ThinkingMiddleware,
        memory: ConversationMemory,
        embedding_provider: EmbeddingProvider | None = None,
    ):
        self.agents = agents
        self.provider_chain = provider_chain
        self.rag = rag
        self.tool_registry = tool_registry
        self.thinking = thinking
        self.memory = memory
        self.embedding_provider = embedding_provider

    @classmethod
    def from_config(
        cls,
        config: RuntimeConfig | None = None,
        repo_root: Path | None = None,
    ) -> "AgentRuntime":
        """Build a fully wired runtime from configuration.

        This is the main factory method.  It:
          1. Loads agent YAML configs
          2. Sets up provider chain
          3. Initializes database + embedding store + RAG
          4. Discovers tools
          5. Wires everything together
        """
        repo_root = repo_root or REPO_ROOT
        config = config or RuntimeConfig()

        # Configure logging
        logging.basicConfig(
            level=getattr(logging, config.log_level.upper(), logging.INFO),
            format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            datefmt="%H:%M:%S",
        )

        # 1. Load agent configs
        agents_dir = repo_root / config.agents_dir
        agents = cls._load_agents(agents_dir)
        logger.info("Loaded %d agents: %s", len(agents), list(agents.keys()))

        # 2. Build provider chain from CEO's preferences (used as default)
        ceo = agents.get("ceo")
        if ceo:
            default_prefs = ceo.provider_preference
        else:
            default_prefs = ["ollama/llama3.2"]
        provider_chain = build_chain_from_preferences(default_prefs)

        # 3. Set up database + embedding store + RAG
        from database.enterprise_db import EnterpriseDB

        db_path = repo_root / config.db_path
        db = EnterpriseDB(db_path)
        db.initialize()

        embedding_store = EmbeddingStore(db_path)
        embedding_store.initialize()

        embedding_provider: EmbeddingProvider | None = None
        rag: HybridRAG | None = None
        try:
            embedding_provider = build_embedding_provider(config.embedding)
            rag = HybridRAG(
                db=db,
                embedding_store=embedding_store,
                embedding_provider=embedding_provider,
                config=config.rag,
            )
            logger.info("Neural RAG initialized (hybrid FTS5 + embeddings)")
        except Exception as exc:
            logger.warning(
                "Embedding provider unavailable (%s); falling back to keyword-only RAG",
                exc,
            )

        # 4. Discover tools
        tool_registry = ToolRegistry()
        set_shared_resources(db, rag, repo_root)
        tool_registry.discover()

        # 5. Wire thinking middleware
        thinking = ThinkingMiddleware(rag=rag)

        # 6. Initialize conversation memory
        memory_path = repo_root / "database" / "data" / "conversations.db"
        memory = ConversationMemory(memory_path)
        memory.initialize()

        return cls(
            agents=agents,
            provider_chain=provider_chain,
            rag=rag,
            tool_registry=tool_registry,
            thinking=thinking,
            memory=memory,
            embedding_provider=embedding_provider,
        )

    async def process(self, task: str, session_id: str = "") -> str:
        """Main entry point: process a task through the agent hierarchy.

        Flow:
          1. CEO classifies the task and picks a delegate
          2. The delegate agent executes with tools + RAG
          3. Result is returned

        Args:
            task: Natural language task or question.
            session_id: Optional session ID for conversation continuity.

        Returns:
            The final text response from the handling agent.
        """
        if not session_id:
            session_id = self.memory.create_session(task)

        # Check if CEO exists; if not, use the first available agent
        ceo_config = self.agents.get("ceo")
        if not ceo_config:
            # No CEO — direct execution with first available agent
            first_agent = next(iter(self.agents.values()))
            logger.info("No CEO agent; using '%s' directly", first_agent.name)
            return await self._execute_agent(first_agent, task, session_id)

        # CEO classifies and delegates
        delegate_name, context = await self._ceo_classify(
            ceo_config, task, session_id
        )

        # Get the delegate agent
        delegate = self.agents.get(delegate_name)
        if not delegate:
            logger.warning(
                "CEO delegated to '%s' but agent not found. Handling directly.",
                delegate_name,
            )
            return await self._execute_agent(ceo_config, task, session_id)

        logger.info(
            "CEO delegated task to %s (%s)",
            delegate.name,
            delegate.title,
        )

        # Execute with the delegate
        result = await self._execute_agent(delegate, task, session_id, context)

        return result

    async def direct_execute(
        self, agent_name: str, task: str, session_id: str = ""
    ) -> str:
        """Execute a task directly with a named agent (bypass CEO).

        Useful for targeted queries where you know which agent should handle it.
        """
        agent_config = self.agents.get(agent_name)
        if not agent_config:
            return f"Agent '{agent_name}' not found. Available: {list(self.agents.keys())}"

        if not session_id:
            session_id = self.memory.create_session(task)

        return await self._execute_agent(agent_config, task, session_id)

    async def index_embeddings(self) -> dict[str, int]:
        """Index all enterprise documents into the embedding store.

        Should be run once on setup and periodically thereafter.
        """
        if self.rag is None:
            return {"error": "RAG not initialized (no embedding provider)"}
        return await self.rag.index_documents()

    # ── Private Methods ──────────────────────────────────────────────────

    async def _ceo_classify(
        self, ceo_config: AgentConfig, task: str, session_id: str
    ) -> tuple[str, str]:
        """Have the CEO classify a task and pick a delegate.

        Returns (delegate_agent_name, context_for_delegate).
        """
        available_agents = {
            name: f"{cfg.title} — {cfg.department}"
            for name, cfg in self.agents.items()
            if name != "ceo"
        }
        agents_desc = "\n".join(
            f"  - {name}: {desc}" for name, desc in available_agents.items()
        )

        classification_prompt = (
            f"You are the CEO. Classify this task and delegate it to the most "
            f"appropriate team member.\n\n"
            f"Available agents:\n{agents_desc}\n\n"
            f"Task: {task}\n\n"
            f"Respond in EXACTLY this format (no other text):\n"
            f"DELEGATE: <agent_name>\n"
            f"CONTEXT: <brief context or instructions for the delegate>"
        )

        executor = self._build_executor(ceo_config)
        raw_response = await executor.execute(
            classification_prompt, session_id=session_id
        )

        # Parse the response
        delegate_name = ""
        context = ""
        for line in raw_response.strip().splitlines():
            line = line.strip()
            if line.upper().startswith("DELEGATE:"):
                delegate_name = line.split(":", 1)[1].strip().lower()
            elif line.upper().startswith("CONTEXT:"):
                context = line.split(":", 1)[1].strip()

        # Validate delegate
        if delegate_name not in self.agents:
            # Try fuzzy matching
            for name in self.agents:
                if name != "ceo" and name in delegate_name:
                    delegate_name = name
                    break
            else:
                # Default to CTO for unrecognized delegation
                delegate_name = next(
                    (n for n in self.agents if n != "ceo"), "ceo"
                )
                logger.warning(
                    "CEO delegation unclear ('%s'), defaulting to '%s'",
                    raw_response[:100],
                    delegate_name,
                )

        return delegate_name, context

    async def _execute_agent(
        self,
        agent_config: AgentConfig,
        task: str,
        session_id: str,
        context: str = "",
    ) -> str:
        """Execute a task with a specific agent."""
        executor = self._build_executor(agent_config)
        return await executor.execute(task, session_id=session_id, context=context)

    def _build_executor(self, agent_config: AgentConfig) -> AgentExecutor:
        """Build an AgentExecutor for a given agent config."""
        # Build per-agent provider chain (falls back to default)
        if agent_config.provider_preference:
            provider = build_chain_from_preferences(agent_config.provider_preference)
        else:
            provider = self.provider_chain

        return AgentExecutor(
            config=agent_config,
            provider=provider,
            tool_registry=self.tool_registry,
            thinking=self.thinking,
            memory=self.memory,
        )

    @staticmethod
    def _load_agents(agents_dir: Path) -> dict[str, AgentConfig]:
        """Load agent configs from YAML files."""
        agents: dict[str, AgentConfig] = {}
        if not agents_dir.exists():
            logger.warning("Agents directory not found: %s", agents_dir)
            return agents

        for yaml_file in sorted(agents_dir.glob("*.yaml")):
            try:
                data = yaml.safe_load(yaml_file.read_text())
                if data is None:
                    continue
                agent = AgentConfig(**data)
                agent_key = yaml_file.stem.lower()
                agents[agent_key] = agent
                logger.debug("Loaded agent config: %s", agent_key)
            except Exception as exc:
                logger.error("Failed to load agent config %s: %s", yaml_file, exc)

        return agents

    # ── Introspection ────────────────────────────────────────────────────

    def list_agents(self) -> list[dict[str, str]]:
        """List all loaded agents."""
        return [
            {
                "name": name,
                "title": cfg.title,
                "department": cfg.department,
                "tools": cfg.tools,
            }
            for name, cfg in self.agents.items()
        ]

    def status(self) -> dict[str, Any]:
        """Runtime status summary."""
        return {
            "agents": len(self.agents),
            "tools": self.tool_registry.names,
            "rag_available": self.rag is not None,
            "embedding_provider": (
                self.embedding_provider.name if self.embedding_provider else None
            ),
            "sessions": self.memory.session_count(),
            "messages": self.memory.message_count(),
        }
