# ai_assistant/application/use_cases/explain_tool.py

from shared.application.result import Result

from ai_assistant.application.queries.get_tool_definition import (
    GetToolDefinitionQuery,
)

from ai_assistant.application.dto.tool_definition_dto import (
    ToolDefinitionDTO,
)

from ai_assistant.application.services.tool_execution_service import (
    ToolExecutionService,
)


class ExplainToolUseCase:

    def __init__(
        self,
        tool_execution_service: ToolExecutionService,
    ):
        self._tool_execution_service = tool_execution_service

    async def execute(
        self,
        query: GetToolDefinitionQuery,
    ) -> Result[ToolDefinitionDTO]:

        tool = self._tool_execution_service.get_tool_definition(
            query.tool_name,
        )

        return Result.success(tool)