# ai_assistant/application/services/tool_execution_service.py

from typing import Any

from ai_assistant.domain.tool_registry import ToolRegistry


class ToolExecutionService:
    """
    Executes registered AI tools.

    Delegates business logic to
    Application Use Cases.
    """

    def __init__(
        self,
        registry: ToolRegistry,
    ) -> None:
        self._registry = registry

    async def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        """
        Locate and execute a tool.
        """

        tool = self._registry.get(tool_name)

        return await tool.execute(**arguments)

    def list_tools(self):
        return self._registry.list()

    def explain_tool(
        self,
        tool_name: str,
    ):
        tool = self._registry.get(tool_name)

        return {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
        }