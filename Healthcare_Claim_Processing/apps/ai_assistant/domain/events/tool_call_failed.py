from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ToolCallFailed(DomainEvent):
    """
    Raised when a tool execution fails.
    """

    conversation_id: UUID

    tool_call_id: UUID

    tool_name: str

    reason: str