"""
Agent Executor
==============

Manages a single agent's message loop: receives a task, runs the
thinking middleware, calls the LLM, handles tool calls, and returns
the final response.

This is the inner loop.  The ``AgentRuntime`` (runtime.py) manages
the outer loop of CEO delegation and multi-agent coordination.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from agents.config import AgentConfig, MessageRole
from agents.memory.conversation import ConversationMemory
from agents.providers.base import ChatProvider, ChatResponse, Message, ToolCall
from agents.thinking import ThinkingMiddleware
from agents.tools import ToolRegistry

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 10  # Prevent infinite tool-calling loops


class AgentExecutor:
    """Executes a single agent's task within a conversation session.

    Flow:
      1. Build system prompt + conversation history
      2. Pre-gen thinking: inject RAG context
      3. Call LLM via provider chain
      4. Post-gen thinking: validate response
      5. If tool calls → execute tools → feed results back → loop
      6. Return final text response
    """

    def __init__(
        self,
        config: AgentConfig,
        provider: ChatProvider,
        tool_registry: ToolRegistry,
        thinking: ThinkingMiddleware,
        memory: ConversationMemory | None = None,
    ):
        self.config = config
        self.provider = provider
        self.tool_registry = tool_registry
        self.thinking = thinking
        self.memory = memory

    async def execute(
        self,
        task: str,
        session_id: str = "",
        context: str = "",
    ) -> str:
        """Execute a task and return the final text response.

        Args:
            task: The task/question to handle.
            session_id: Session ID for conversation tracking.
            context: Additional context from the delegating agent.

        Returns:
            The agent's final text response.
        """
        # Build initial messages
        messages = self._build_messages(task, context, session_id)

        # Store user message
        if self.memory and session_id:
            self.memory.add_message(
                session_id,
                self.config.name,
                Message(role=MessageRole.USER, content=task),
            )

        # Get tool specs for this agent
        tool_specs = self.tool_registry.get_specs(self.config.tools or None)

        for round_num in range(MAX_TOOL_ROUNDS):
            # Pre-gen: inject RAG context (only on first round)
            if round_num == 0:
                messages = await self.thinking.pre_gen(self.config, messages)

            # Call LLM
            response = await self.provider.chat(
                messages,
                tools=tool_specs if tool_specs else None,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            # Post-gen: validate
            response = self.thinking.post_gen(self.config, response, messages)

            # If no tool calls, we're done
            if not response.message.tool_calls:
                final_text = response.message.content
                if self.memory and session_id:
                    self.memory.add_message(
                        session_id,
                        self.config.name,
                        response.message,
                    )
                return final_text

            # Handle tool calls
            messages.append(response.message)
            tool_results = await self._execute_tool_calls(response.message.tool_calls)

            for result_msg in tool_results:
                messages.append(result_msg)
                if self.memory and session_id:
                    self.memory.add_message(
                        session_id, self.config.name, result_msg
                    )

            logger.info(
                "Agent %s completed tool round %d/%d (%d calls)",
                self.config.name,
                round_num + 1,
                MAX_TOOL_ROUNDS,
                len(response.message.tool_calls),
            )

        # Exhausted tool rounds — ask for final answer
        messages.append(
            Message(
                role=MessageRole.USER,
                content="Please provide your final answer based on the tool results above.",
            )
        )
        response = await self.provider.chat(messages)
        return response.message.content

    def _build_messages(
        self, task: str, context: str, session_id: str
    ) -> list[Message]:
        """Build the initial message list with system prompt + history."""
        messages: list[Message] = []

        # System prompt
        messages.append(
            Message(role=MessageRole.SYSTEM, content=self.config.system_prompt)
        )

        # Conversation history (if available)
        if self.memory and session_id:
            history = self.memory.get_buffer(
                session_id,
                self.config.name,
                buffer_size=self.config.memory.conversation_buffer,
            )
            # Only add non-system messages from history
            for msg in history:
                if msg.role != MessageRole.SYSTEM:
                    messages.append(msg)

        # Delegation context
        if context:
            messages.append(
                Message(
                    role=MessageRole.SYSTEM,
                    content=f"Context from delegating agent:\n{context}",
                )
            )

        # The actual task
        messages.append(Message(role=MessageRole.USER, content=task))

        return messages

    async def _execute_tool_calls(
        self, tool_calls: list[ToolCall]
    ) -> list[Message]:
        """Execute tool calls and return result messages."""
        results: list[Message] = []
        for tc in tool_calls:
            logger.debug(
                "Executing tool '%s' with args: %s",
                tc.function,
                str(tc.arguments)[:200],
            )
            result = await self.tool_registry.execute(tc.function, tc.arguments)

            # Serialize result to string
            if isinstance(result, (dict, list)):
                result_str = json.dumps(result, indent=2, default=str)
            else:
                result_str = str(result)

            # Truncate very long results
            if len(result_str) > 4000:
                result_str = result_str[:4000] + "\n\n... (truncated)"

            results.append(
                Message(
                    role=MessageRole.TOOL,
                    content=result_str,
                    tool_call_id=tc.id,
                    name=tc.function,
                )
            )

        return results
