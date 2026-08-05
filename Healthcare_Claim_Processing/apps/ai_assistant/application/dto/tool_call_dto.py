from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolCallDTO:
    """
    Represents a tool selected by the LLM.
    """

    tool_name: str

    arguments: dict[str, Any]