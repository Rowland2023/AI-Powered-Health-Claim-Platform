from dataclasses import dataclass
from uuid import UUID

from shared.domain.domain_event import DomainEvent


@dataclass(frozen=True)
class ConversationStarted(DomainEvent):
    """
    Raised when a new AI conversation begins.
    """

    conversation_id: UUID
    user_id: UUID