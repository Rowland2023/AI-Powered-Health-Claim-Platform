from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ToolCallCompleted(DomainEvent):
    """
    Raised after successful tool execution.
    """

    conversation_id: UUID

    tool_call_id: UUID

    tool_name: str