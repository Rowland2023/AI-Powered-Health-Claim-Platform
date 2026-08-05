from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ToolCallRequested(DomainEvent):
    """
    Raised before a tool executes.
    """

    conversation_id: UUID

    tool_call_id: UUID

    tool_name: str