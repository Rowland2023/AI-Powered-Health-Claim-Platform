from dataclasses import dataclass


@dataclass(frozen=True)
class GetToolDefinitionQuery:
    """
    Retrieve metadata for a tool.
    """

    tool_name: str