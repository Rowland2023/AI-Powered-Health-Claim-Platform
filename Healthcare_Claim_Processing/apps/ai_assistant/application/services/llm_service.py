# ai_assistant/application/services/llm_service.py

from abc import ABC, abstractmethod

from ai_assistant.application.commands.execute_prompt import (
    ExecutePromptCommand,
)
from ai_assistant.application.dto.ai_response_dto import AIResponseDTO


class LLMService(ABC):
    """
    Port for Large Language Model providers.

    Implementations live in infrastructure.llm.
    """

    @abstractmethod
    async def generate_response(
        self,
        command: ExecutePromptCommand,
    ) -> AIResponseDTO:
        """
        Generates an AI response.

        May include one or more tool calls.
        """
        raise NotImplementedError

    @abstractmethod
    async def summarize(
        self,
        text: str,
    ) -> str:
        """
        Summarize arbitrary text.
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