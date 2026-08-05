from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class UserMessageAdded(DomainEvent):
    """
    Raised when a user sends a message.
    """

    conversation_id: UUID
    message_id: UUID