from abc import ABC, abstractmethod

from ai_assistant.application.dto.ai_response import AIResponseDTO
from ai_assistant.application.commands.execute_prompt import ExecutePromptCommand


class LLMProvider(ABC):

    @abstractmethod
    async def execute(
        self,
        command: ExecutePromptCommand,
    ) -> AIResponseDTO:
        """
        Translate natural language into tool calls.
        """