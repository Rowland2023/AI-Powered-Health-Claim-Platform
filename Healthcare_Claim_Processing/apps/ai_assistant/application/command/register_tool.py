from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterToolCommand:
    """
    Register an AI tool.
    """

    tool_name: str

    description: str