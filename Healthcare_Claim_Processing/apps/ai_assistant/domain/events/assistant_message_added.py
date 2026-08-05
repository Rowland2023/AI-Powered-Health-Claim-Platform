from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class AssistantMessageAdded(DomainEvent):
    """
    Raised when the AI generates a response.
    """

    conversation_id: UUID
    message_id: UUID