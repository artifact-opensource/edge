"""
Tool Registry
=============

Provides the ``@tool`` decorator for declaring Python functions as
LLM-callable tools, and the ``ToolRegistry`` that manages them.

Tools are decorated Python functions with type hints.  The decorator
auto-generates the JSON Schema that LLMs need for function calling.

Usage::

    from agents.tools import tool, ToolRegistry

    @tool("search_documents", "Search enterprise documents")
    async def search_documents(query: str, limit: int = 5) -> list[dict]:
        ...

    registry = ToolRegistry()
    registry.discover()  # Auto-discovers all @tool functions
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, get_type_hints

logger = logging.getLogger(__name__)

# ── Global tool store ────────────────────────────────────────────────────────

_REGISTERED_TOOLS: dict[str, "Tool"] = {}


@dataclass
class Tool:
    """A registered tool with metadata and schema."""

    name: str
    description: str
    func: Callable[..., Any]
    parameters: dict[str, Any] = field(default_factory=dict)
    is_async: bool = False

    def to_openai_spec(self) -> dict[str, Any]:
        """Generate OpenAI-compatible tool specification for function calling."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


def _python_type_to_json_schema(typ: type) -> dict[str, Any]:
    """Map Python type hints to JSON Schema types."""
    origin = getattr(typ, "__origin__", None)

    if typ is str:
        return {"type": "string"}
    elif typ is int:
        return {"type": "integer"}
    elif typ is float:
        return {"type": "number"}
    elif typ is bool:
        return {"type": "boolean"}
    elif origin is list:
        args = getattr(typ, "__args__", (Any,))
        items = _python_type_to_json_schema(args[0]) if args else {}
        return {"type": "array", "items": items}
    elif origin is dict:
        return {"type": "object"}
    else:
        return {"type": "string"}


def _build_parameters_schema(func: Callable) -> dict[str, Any]:
    """Build JSON Schema from function signature + type hints."""
    sig = inspect.signature(func)
    try:
        hints = get_type_hints(func)
    except Exception:
        hints = {}

    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name in ("self", "cls"):
            continue

        prop: dict[str, Any] = {}
        if name in hints:
            prop.update(_python_type_to_json_schema(hints[name]))
        else:
            prop["type"] = "string"

        # Extract description from docstring (Args section)
        doc = inspect.getdoc(func) or ""
        for line in doc.split("\n"):
            stripped = line.strip()
            if stripped.startswith(f"{name}:") or stripped.startswith(f"{name} "):
                desc = stripped.split(":", 1)[-1].strip() if ":" in stripped else ""
                if desc:
                    prop["description"] = desc
                break

        if param.default is not inspect.Parameter.empty:
            prop["default"] = param.default
        else:
            required.append(name)

        properties[name] = prop

    schema: dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    return schema


def tool(name: str, description: str) -> Callable:
    """Decorator to register a function as an LLM-callable tool.

    Args:
        name: Unique tool name for function calling.
        description: Human-readable description shown to the LLM.
    """

    def decorator(func: Callable) -> Callable:
        schema = _build_parameters_schema(func)
        t = Tool(
            name=name,
            description=description,
            func=func,
            parameters=schema,
            is_async=asyncio.iscoroutinefunction(func),
        )
        _REGISTERED_TOOLS[name] = t
        func._tool = t  # type: ignore[attr-defined]
        return func

    return decorator


class ToolRegistry:
    """Manages discovered tools and provides lookup + execution."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def discover(self) -> None:
        """Import all tool modules and register their @tool functions."""
        # Import enterprise tools to trigger registration
        try:
            import agents.tools.enterprise  # noqa: F401
        except ImportError as exc:
            logger.warning("Could not import enterprise tools: %s", exc)

        # Copy all registered tools
        self._tools.update(_REGISTERED_TOOLS)
        logger.info("Discovered %d tools: %s", len(self._tools), list(self._tools.keys()))

    def register(self, t: Tool) -> None:
        """Manually register a tool."""
        self._tools[t.name] = t

    def get(self, name: str) -> Tool | None:
        """Look up a tool by name."""
        return self._tools.get(name)

    def list_tools(self, names: list[str] | None = None) -> list[Tool]:
        """List tools, optionally filtered by name."""
        if names is None:
            return list(self._tools.values())
        return [self._tools[n] for n in names if n in self._tools]

    def get_specs(self, names: list[str] | None = None) -> list[dict[str, Any]]:
        """Get OpenAI-compatible tool specs for a subset of tools."""
        return [t.to_openai_spec() for t in self.list_tools(names)]

    async def execute(self, name: str, arguments: dict[str, Any]) -> Any:
        """Execute a tool by name with the given arguments.

        Handles both sync and async tool functions.
        """
        t = self._tools.get(name)
        if t is None:
            return {"error": f"Unknown tool: {name}"}

        try:
            if t.is_async:
                result = await t.func(**arguments)
            else:
                result = t.func(**arguments)
            return result
        except Exception as exc:
            logger.error("Tool '%s' failed: %s", name, exc)
            return {"error": f"Tool execution failed: {exc}"}

    @property
    def names(self) -> list[str]:
        return list(self._tools.keys())
