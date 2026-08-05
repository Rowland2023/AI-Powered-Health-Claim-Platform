# ai_assistant/application/use_cases/execute_tool_call.py

from shared.application.result import Result

from ai_assistant.application.commands.execute_tool import ExecuteToolCommand
from ai_assistant.application.dto.tool_result_dto import ToolResultDTO
from ai_assistant.application.services.tool_execution_service import (
    ToolExecutionService,
)


class ExecuteToolCallUseCase:

    def __init__(
        self,
        tool_execution_service: ToolExecutionService,
    ):
        self._tool_execution_service = tool_execution_service

    async def execute(
        self,
        command: ExecuteToolCommand,
    ) -> Result[ToolResultDTO]:

        result = await self._tool_execution_service.execute(
            command.tool_name,
            command.arguments,
        )

        return Result.success(result)