"""
DAG Workflow Engine
===================

Executes workflow definitions as Directed Acyclic Graphs.

Each node in the DAG is one of:
  - ``AGENT``       — Delegates to a named agent
  - ``PYTHON``      — Runs a registered tool / function
  - ``HUMAN``       — Pauses for human approval
  - ``CONDITIONAL`` — Branches based on a condition

Nodes within the same topological layer execute concurrently.
Inter-layer dependencies are respected via topological sort.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable

from agents.config import NodeType, WorkflowConfig, WorkflowNodeConfig

logger = logging.getLogger(__name__)


@dataclass
class NodeResult:
    """Result of executing a single workflow node."""

    node_id: str
    status: str = "pending"  # pending, running, completed, failed, skipped, waiting_approval
    output: Any = None
    error: str = ""
    duration_ms: float = 0


@dataclass
class WorkflowResult:
    """Result of executing an entire workflow."""

    workflow_id: str
    status: str = "pending"  # pending, running, completed, failed, partial
    node_results: dict[str, NodeResult] = field(default_factory=dict)
    duration_ms: float = 0

    @property
    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = defaultdict(int)
        for nr in self.node_results.values():
            counts[nr.status] += 1
        return dict(counts)


class DAGExecutor:
    """Executes workflow DAGs with topological ordering and parallel layers.

    Usage:
        executor = DAGExecutor(
            agent_handler=...,  # async fn(node, context) -> str
            python_handler=..., # async fn(node, context) -> Any
        )
        result = await executor.execute(workflow, context)
    """

    def __init__(
        self,
        agent_handler: Callable | None = None,
        python_handler: Callable | None = None,
        human_handler: Callable | None = None,
    ):
        self.agent_handler = agent_handler
        self.python_handler = python_handler
        self.human_handler = human_handler or self._default_human_handler

    async def execute(
        self,
        workflow: WorkflowConfig,
        context: dict[str, Any] | None = None,
    ) -> WorkflowResult:
        """Execute a workflow DAG.

        Args:
            workflow: The workflow definition.
            context: Shared context dict passed to all nodes.

        Returns:
            WorkflowResult with per-node results.
        """
        context = context or {}
        result = WorkflowResult(workflow_id=workflow.id, status="running")
        start_time = time.monotonic()

        # Filter to enabled nodes
        enabled_nodes = [n for n in workflow.nodes if n.enabled]
        if not enabled_nodes:
            result.status = "completed"
            result.duration_ms = (time.monotonic() - start_time) * 1000
            return result

        # Topological sort into layers
        layers = self._topological_sort(enabled_nodes)
        logger.info(
            "Workflow '%s': %d nodes in %d layers",
            workflow.name,
            len(enabled_nodes),
            len(layers),
        )

        # Execute layer by layer
        all_ok = True
        for layer_idx, layer in enumerate(layers):
            logger.info(
                "Executing layer %d/%d: %s",
                layer_idx + 1,
                len(layers),
                [n.id for n in layer],
            )

            # Check dependencies are satisfied
            layer_to_run = []
            for node in layer:
                deps_ok = all(
                    result.node_results.get(dep, NodeResult(node_id=dep)).status == "completed"
                    for dep in node.depends_on
                )
                if deps_ok:
                    layer_to_run.append(node)
                else:
                    nr = NodeResult(node_id=node.id, status="skipped", error="dependency failed")
                    result.node_results[node.id] = nr

            # Execute nodes in this layer concurrently
            tasks = [
                self._execute_node(node, context, result)
                for node in layer_to_run
            ]
            layer_results = await asyncio.gather(*tasks, return_exceptions=True)

            for node, lr in zip(layer_to_run, layer_results):
                if isinstance(lr, Exception):
                    nr = NodeResult(
                        node_id=node.id, status="failed", error=str(lr)
                    )
                    result.node_results[node.id] = nr
                    all_ok = False

        result.status = "completed" if all_ok else "partial"
        result.duration_ms = (time.monotonic() - start_time) * 1000
        logger.info(
            "Workflow '%s' %s in %.0fms: %s",
            workflow.name,
            result.status,
            result.duration_ms,
            result.summary,
        )
        return result

    async def _execute_node(
        self,
        node: WorkflowNodeConfig,
        context: dict[str, Any],
        workflow_result: WorkflowResult,
    ) -> None:
        """Execute a single node based on its type."""
        nr = NodeResult(node_id=node.id, status="running")
        start = time.monotonic()

        try:
            if node.type == NodeType.AGENT:
                if self.agent_handler:
                    output = await self.agent_handler(node, context)
                else:
                    output = f"[agent:{node.agent}] No agent handler configured"
                nr.output = output

            elif node.type == NodeType.PYTHON:
                if self.python_handler:
                    output = await self.python_handler(node, context)
                else:
                    output = f"[python:{node.function}] No python handler configured"
                nr.output = output

            elif node.type == NodeType.HUMAN:
                output = await self.human_handler(node, context)
                nr.output = output

            elif node.type == NodeType.CONDITIONAL:
                # Evaluate condition against context
                condition_result = self._eval_condition(node.condition, context)
                nr.output = {
                    "condition": node.condition,
                    "result": condition_result,
                    "branch": node.true_branch if condition_result else node.false_branch,
                }

            nr.status = "completed"

        except Exception as exc:
            nr.status = "failed"
            nr.error = str(exc)
            logger.error("Node '%s' failed: %s", node.id, exc)

        nr.duration_ms = (time.monotonic() - start) * 1000
        workflow_result.node_results[node.id] = nr

        # Store output in context for downstream nodes
        context[f"node:{node.id}"] = nr.output

    def _topological_sort(
        self, nodes: list[WorkflowNodeConfig]
    ) -> list[list[WorkflowNodeConfig]]:
        """Sort nodes into execution layers via Kahn's algorithm.

        Nodes in the same layer have no dependencies on each other
        and can execute concurrently.
        """
        node_map = {n.id: n for n in nodes}
        in_degree: dict[str, int] = {n.id: 0 for n in nodes}
        adjacency: dict[str, list[str]] = {n.id: [] for n in nodes}

        for node in nodes:
            for dep in node.depends_on:
                if dep in node_map:
                    adjacency[dep].append(node.id)
                    in_degree[node.id] += 1

        # BFS by layers
        layers: list[list[WorkflowNodeConfig]] = []
        queue = [nid for nid, deg in in_degree.items() if deg == 0]

        while queue:
            layer = [node_map[nid] for nid in queue if nid in node_map]
            if not layer:
                break
            layers.append(layer)

            next_queue: list[str] = []
            for nid in queue:
                for neighbor in adjacency.get(nid, []):
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_queue.append(neighbor)
            queue = next_queue

        # Detect cycles
        remaining = [n for n in nodes if n.id not in {n.id for layer in layers for n in layer}]
        if remaining:
            logger.warning(
                "Workflow has cycles involving: %s — appending as final layer",
                [n.id for n in remaining],
            )
            layers.append(remaining)

        return layers

    @staticmethod
    def _eval_condition(condition: str, context: dict[str, Any]) -> bool:
        """Safely evaluate a simple condition expression against context.

        Only supports basic comparisons, not arbitrary code execution.
        """
        if not condition:
            return True
        try:
            # Simple key-based lookup: "node:check_result == passed"
            parts = condition.split()
            if len(parts) == 3:
                key, op, value = parts
                actual = str(context.get(key, ""))
                if op == "==":
                    return actual == value
                elif op == "!=":
                    return actual != value
                elif op == ">":
                    return float(actual) > float(value)
                elif op == "<":
                    return float(actual) < float(value)
            return bool(context.get(condition, False))
        except Exception:
            return True

    @staticmethod
    async def _default_human_handler(
        node: WorkflowNodeConfig, context: dict[str, Any]
    ) -> str:
        """Default human approval handler — auto-approves in non-interactive mode."""
        logger.info(
            "Human approval required for '%s' (approvers: %s). Auto-approving.",
            node.name,
            node.approvers,
        )
        return "auto-approved (non-interactive mode)"
