from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExecuteToolCommand:
    """
    Command to execute a single AI tool.
    """

    tool_name: str

    arguments: dict[str, Any]