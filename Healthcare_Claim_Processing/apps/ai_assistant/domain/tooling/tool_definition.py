from dataclasses import dataclass

from .tool_parameter import ToolParameter


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """
    Immutable description of an AI tool.
    """

    name: str

    description: str

    parameters: list[ToolParameter]