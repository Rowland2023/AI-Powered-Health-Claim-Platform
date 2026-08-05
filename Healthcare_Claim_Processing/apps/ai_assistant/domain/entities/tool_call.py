from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from ..value_objects.tool_name import ToolName
from ..value_objects.tool_argument import ToolArgument
from ..value_objects.tool_result import ToolResult


@dataclass(slots=True)
class ToolCall:
    """
    Represents a validated AI tool invocation.

    A ToolCall is an Entity because it has its own identity
    and lifecycle within a Conversation.
    """

    id: UUID

    tool_name: ToolName

    arguments: list[ToolArgument]

    result: ToolResult | None = None

    executed_at: datetime | None = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    @classmethod
    def create(
        cls,
        tool_name: ToolName,
        arguments: list[ToolArgument],
    ) -> "ToolCall":

        return cls(
            id=uuid4(),
            tool_name=tool_name,
            arguments=arguments,
        )

    def complete(
        self,
        result: ToolResult,
    ) -> None:

        self.result = result
        self.executed_at = datetime.now(UTC)