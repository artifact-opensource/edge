"""
CLI Entry Point
===============

Usage::

    # CEO delegation (default)
    python -m agents "What is our GRC compliance status?"

    # Direct agent execution
    python -m agents --agent cto "List all infrastructure workflows"

    # Index embeddings into the neural RAG
    python -m agents --index

    # Show runtime status
    python -m agents --status

    # List available agents
    python -m agents --list-agents

    # List available tools
    python -m agents --list-tools
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

from agents.config import RuntimeConfig
from agents.runtime import AgentRuntime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="agents",
        description="Artifact Virtual Multi-Agent Runtime",
    )
    parser.add_argument(
        "task",
        nargs="?",
        default="",
        help="Task to process (natural language)",
    )
    parser.add_argument(
        "--agent",
        "-a",
        default="",
        help="Execute directly with a specific agent (bypass CEO)",
    )
    parser.add_argument(
        "--index",
        action="store_true",
        help="Index all documents into the embedding store",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show runtime status",
    )
    parser.add_argument(
        "--list-agents",
        action="store_true",
        help="List available agents",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List available tools",
    )
    parser.add_argument(
        "--provider",
        default="",
        help="Override provider (e.g., 'ollama/llama3.2', 'openai_compat/gpt-4o@https://api.openai.com/v1?key=sk-...')",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )
    return parser.parse_args()


async def main() -> int:
    args = parse_args()

    # Build runtime config
    config = RuntimeConfig(log_level=args.log_level)

    # Initialize runtime
    try:
        runtime = AgentRuntime.from_config(config)
    except Exception as exc:
        print(f"Failed to initialize runtime: {exc}", file=sys.stderr)
        return 1

    # Handle commands
    if args.status:
        status = runtime.status()
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print("=== Agent Runtime Status ===")
            for key, value in status.items():
                print(f"  {key}: {value}")
        return 0

    if args.list_agents:
        agents = runtime.list_agents()
        if args.json:
            print(json.dumps(agents, indent=2))
        else:
            print("=== Available Agents ===")
            for a in agents:
                print(f"  {a['name']:8s}  {a['title']:35s}  [{a['department']}]")
                if a.get("tools"):
                    print(f"           tools: {', '.join(a['tools'][:5])}{'...' if len(a['tools']) > 5 else ''}")
        return 0

    if args.list_tools:
        tools = runtime.tool_registry.list_tools()
        if args.json:
            specs = [t.to_openai_spec() for t in tools]
            print(json.dumps(specs, indent=2))
        else:
            print("=== Available Tools ===")
            for t in tools:
                print(f"  {t.name:30s}  {t.description}")
        return 0

    if args.index:
        print("Indexing documents into embedding store...")
        stats = await runtime.index_embeddings()
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            for key, value in stats.items():
                print(f"  {key}: {value}")
        return 0

    if not args.task:
        print("No task provided. Use --help for usage.", file=sys.stderr)
        return 1

    # Execute task
    print(f"Processing: {args.task}\n")

    if args.agent:
        result = await runtime.direct_execute(args.agent, args.task)
    else:
        result = await runtime.process(args.task)

    if args.json:
        print(json.dumps({"result": result}))
    else:
        print(result)

    return 0


def cli_entry() -> None:
    """Sync entry point for the CLI."""
    sys.exit(asyncio.run(main()))


if __name__ == "__main__":
    cli_entry()
