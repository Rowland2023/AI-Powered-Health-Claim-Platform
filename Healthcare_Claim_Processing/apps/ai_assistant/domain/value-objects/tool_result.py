from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ToolResult:
    """
    Represents the outcome of executing an AI tool.
    """

    success: bool

    data: Any = None

    message: str | None = None

    error: str | None = None

    @classmethod
    def success_result(
        cls,
        data: Any = None,
        message: str | None = None,
    ) -> "ToolResult":

        return cls(
            success=True,
            data=data,
            message=message,
        )

    @classmethod
    def failure(
        cls,
        error: str,
    ) -> "ToolResult":

        return cls(
            success=False,
            error=error,
        )