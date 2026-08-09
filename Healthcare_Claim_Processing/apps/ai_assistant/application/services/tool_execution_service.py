
from __future__ import annotations

from typing import Any

from ai_assistant.domain.tool import Tool
from ai_assistant.domain.tool_registry import ToolRegistry


class ToolExecutionService:
    """
    Application service responsible for executing and managing
    registered AI tools.
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
        Locate and execute a registered tool.
        """

        tool = self._registry.get(tool_name)

        return await tool.execute(**arguments)

    def register(
        self,
        tool: Tool,
    ) -> None:
        """
        Register a tool.
        """

        self._registry.register(tool)

    def list_tools(self):
        """
        Return definitions of all registered tools.
        """

        return self._registry.definitions()

    def get_tool_definition(
        self,
        tool_name: str,
    ):
        """
        Return the public definition of a registered tool.
        """

        tool = self._registry.get(tool_name)

        return tool.definition