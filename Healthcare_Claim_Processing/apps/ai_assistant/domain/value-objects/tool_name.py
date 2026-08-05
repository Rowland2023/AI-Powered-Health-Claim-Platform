from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolName:
    """
    Immutable value object representing the name of an AI tool.
    """

    value: str

    def __post_init__(self):
        if not self.value.strip():
            raise ValueError("Tool name cannot be empty.")

    def __str__(self) -> str:
        return self.value