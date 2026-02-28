"""
Artifact Virtual — Multi-Agent Runtime
=======================================

A lightweight, async-first multi-agent orchestration system built on top
of the enterprise SQLite + FTS5 database.  Design principles:

  1. **Local-first** – Ollama is the default provider; cloud is opt-in.
  2. **Provider-agnostic** – Any OpenAI-compatible endpoint works.
  3. **Honest RAG** – Hybrid FTS5 keyword + neural embedding search.
  4. **Tools-as-functions** – Decorated Python functions, auto-schema.
  5. **DAG workflows** – JSON workflow definitions get a real runtime.
  6. **Thinking phases** – Pre-gen context retrieval, post-gen reflection.

Quick start::

    from agents import AgentRuntime

    runtime = AgentRuntime.from_config("agents/configs")
    result = asyncio.run(runtime.process("What is our GRC compliance status?"))

Copyright (c) 2025-2026 Artifact Virtual (SMC-Private) Limited
"""

__version__ = "1.0.0"
