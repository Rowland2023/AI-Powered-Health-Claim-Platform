# ai_assistant/application/use_cases/list_tools.py

from shared.application.result import Result

from ai_assistant.application.dto.tool_definition_dto import (
    ToolDefinitionDTO,
)

from ai_assistant.application.services.tool_execution_service import (
    ToolExecutionService,
)


class ListToolsUseCase:

    def __init__(
        self,
        tool_execution_service: ToolExecutionService,
    ):
        self._tool_execution_service = tool_execution_service

    async def execute(self) -> Result[list[ToolDefinitionDTO]]:

        tools = self._tool_execution_service.list_tools()

        return Result.success(tools)