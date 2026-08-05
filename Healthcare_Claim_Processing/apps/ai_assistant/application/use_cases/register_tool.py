# ai_assistant/application/use_cases/register_tool.py

from shared.application.result import Result

from ai_assistant.application.commands.register_tool import RegisterToolCommand
from ai_assistant.application.services.tool_execution_service import (
    ToolExecutionService,
)


class RegisterToolUseCase:

    def __init__(
        self,
        tool_execution_service: ToolExecutionService,
    ):
        self._tool_execution_service = tool_execution_service

    async def execute(
        self,
        command: RegisterToolCommand,
    ) -> Result[None]:

        self._tool_execution_service.register(command.tool)

        return Result.success(None)