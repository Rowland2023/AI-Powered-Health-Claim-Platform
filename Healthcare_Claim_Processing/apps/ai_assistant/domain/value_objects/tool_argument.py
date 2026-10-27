from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ToolArgument:
    """
    Represents a validated argument supplied to an AI tool.
    """

    name: str
    value: Any

    def __post_init__(self):

        if not self.name.strip():
            raise ValueError(
                "Argument name cannot be empty."
            )