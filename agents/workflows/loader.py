"""
Workflow Loader
===============

Loads the 14 existing JSON workflow definitions and normalizes them
into ``WorkflowConfig`` objects with proper DAG node/edge structures.

The JSON files have two formats:
  1. ``tasks`` — flat list with ``depends_on`` fields
  2. ``workflow_steps`` — numbered steps with implicit sequence

Both are normalized into DAG nodes.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from agents.config import NodeType, WorkflowConfig, WorkflowNodeConfig

logger = logging.getLogger(__name__)


def load_workflow(path: Path | str) -> WorkflowConfig | None:
    """Load a single workflow JSON file and normalize to WorkflowConfig."""
    path = Path(path)
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        logger.error("Failed to load workflow %s: %s", path, exc)
        return None

    workflow_id = path.stem
    nodes = _extract_nodes(data)

    return WorkflowConfig(
        id=workflow_id,
        name=data.get("name", workflow_id),
        description=data.get("description", ""),
        department=data.get("department", ""),
        type=data.get("type", ""),
        enabled=data.get("enabled", False),
        schedule=data.get("schedule", ""),
        nodes=nodes,
        metadata={
            "source_file": str(path),
            "triggers": data.get("triggers", {}),
            "notifications": data.get("notifications", {}),
            "compliance": data.get("compliance", {}),
        },
    )


def load_all_workflows(workflows_dir: Path | str) -> list[WorkflowConfig]:
    """Load all workflow JSON files from a directory tree."""
    workflows_dir = Path(workflows_dir)
    workflows = []
    if not workflows_dir.exists():
        logger.warning("Workflows directory not found: %s", workflows_dir)
        return workflows

    for json_file in sorted(workflows_dir.rglob("*.json")):
        wf = load_workflow(json_file)
        if wf is not None:
            workflows.append(wf)

    logger.info("Loaded %d workflow definitions", len(workflows))
    return workflows


def _extract_nodes(data: dict[str, Any]) -> list[WorkflowNodeConfig]:
    """Extract and normalize workflow nodes from JSON data.

    Handles both ``tasks`` (flat list) and ``workflow_steps`` (numbered) formats.
    """
    nodes: list[WorkflowNodeConfig] = []

    # Format 1: tasks list (most common)
    if "tasks" in data:
        for i, task in enumerate(data["tasks"]):
            node = _task_to_node(task, i)
            nodes.append(node)

    # Format 2: workflow_steps (numbered steps)
    elif "workflow_steps" in data:
        for step in data["workflow_steps"]:
            node = _step_to_node(step)
            nodes.append(node)

    return nodes


def _task_to_node(task: dict[str, Any], index: int) -> WorkflowNodeConfig:
    """Convert a ``tasks`` entry to a WorkflowNodeConfig."""
    name = task.get("name", f"task_{index}")

    # Determine node type
    node_type = NodeType.PYTHON  # Default
    if "approvers" in task or "assignee_role" in task:
        node_type = NodeType.HUMAN
    elif "agent" in task or "prompt_template" in task:
        node_type = NodeType.AGENT
    elif "condition" in task:
        node_type = NodeType.CONDITIONAL

    # Extract dependencies
    depends_on = task.get("depends_on", [])
    if isinstance(depends_on, str):
        depends_on = [depends_on]

    # Collect all config data (excluding structural fields)
    config = {
        k: v
        for k, v in task.items()
        if k not in ("name", "enabled", "depends_on", "approvers", "agent", "condition")
    }

    return WorkflowNodeConfig(
        id=name,
        name=name,
        type=node_type,
        enabled=task.get("enabled", True),
        depends_on=depends_on,
        config=config,
        approvers=task.get("approvers", []),
        agent=task.get("agent", ""),
        condition=task.get("condition", ""),
    )


def _step_to_node(step: dict[str, Any]) -> WorkflowNodeConfig:
    """Convert a ``workflow_steps`` entry to a WorkflowNodeConfig."""
    name = step.get("name", f"step_{step.get('step', 0)}")
    step_num = step.get("step", 0)

    # Determine node type
    node_type = NodeType.PYTHON
    if "assignee_role" in step or "approvers" in step:
        node_type = NodeType.HUMAN
    elif "agent" in step:
        node_type = NodeType.AGENT

    # Sequential dependency: each step depends on the previous
    depends_on = []
    if step.get("depends_on"):
        dep = step["depends_on"]
        depends_on = [dep] if isinstance(dep, str) else dep

    config = {
        k: v
        for k, v in step.items()
        if k not in ("step", "name", "enabled", "depends_on", "approvers", "assignee_role")
    }

    return WorkflowNodeConfig(
        id=name,
        name=name,
        type=node_type,
        enabled=step.get("enabled", True),
        depends_on=depends_on,
        config=config,
        approvers=step.get("approvers", []) or (
            [step["assignee_role"]] if "assignee_role" in step else []
        ),
    )
