from .tool import Tool


class ToolRegistry:
    """
    Registry of all AI tools available to the assistant.
    """

    def __init__(self):

        self._tools: dict[str, Tool] = {}

    def register(
        self,
        tool: Tool,
    ) -> None:

        self._tools[
            tool.definition.name
        ] = tool

    def register_many(
        self,
        tools: list[Tool],
    ) -> None:

        for tool in tools:
            self.register(tool)

    def get(
        self,
        name: str,
    ) -> Tool:

        return self._tools[name]

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def definitions(
        self,
    ) -> list:

        return [
            tool.definition
            for tool in self._tools.values()
        ]

    def all(self):

        return list(
            self._tools.values()
        )