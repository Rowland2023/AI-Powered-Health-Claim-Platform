
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ai_assistant.application.commands.execute_prompt import (
    ExecutePromptCommand,
)

from ai_assistant.application.dto.ai_response_dto import (
    AIResponseDTO,
)


class LLMService(ABC):
    """
    Application port for Large Language Model providers.

    Infrastructure provides the concrete implementation.

    The application layer does not know whether the provider
    is OpenAI, Anthropic, Gemini, a local model, or another
    LLM provider.
    """

    @abstractmethod
    async def generate_tool_calls(
        self,
        *,
        command: ExecutePromptCommand,
        available_tools: list[Any],
        conversation_history: list[dict],
    ) -> list[Any]:
        """
        Ask the LLM to determine which registered tools,
        if any, should be executed.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_final_response(
        self,
        *,
        prompt: str,
        tool_results: list[Any],
        conversation_history: list[dict],
    ) -> AIResponseDTO:
        """
        Generate the final response after tool execution.
        """
        raise NotImplementedError

    @abstractmethod
    async def summarize(
        self,
        history: list[dict],
    ) -> AIResponseDTO:
        """
        Summarize a conversation history.
        """
        raise NotImplementedError

    @abstractmethod
    async def explain(
        self,
        topic: str,
    ) -> str:
        """
        Explain a topic in natural language.
        """
        raise NotImplementedError
