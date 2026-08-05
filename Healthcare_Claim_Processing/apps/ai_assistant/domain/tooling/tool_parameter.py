from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ToolParameter:
    """
    Describes one parameter accepted by a Tool.
    """

    name: str

    type: str

    description: str

    required: bool = True