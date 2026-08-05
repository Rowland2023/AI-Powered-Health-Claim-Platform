from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ToolResultDTO:
    """
    Result returned by a tool.
    """

    tool_name: str

    success: bool

    result: Any

    message: str | None = None