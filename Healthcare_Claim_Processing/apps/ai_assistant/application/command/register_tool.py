
from __future__ import annotations

from dataclasses import dataclass

from ai_assistant.domain.tool import Tool


@dataclass(frozen=True)
class RegisterToolCommand:
    """
    Command for registering an executable AI tool.

    The application layer receives the tool abstraction,
    not infrastructure-specific implementation details.
    """

    tool: Tool
