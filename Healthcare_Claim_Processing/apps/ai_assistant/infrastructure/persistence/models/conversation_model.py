from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ai_assistant.domain.value_objects.conversation_status import (
    ConversationStatus,
)


@dataclass(slots=True)
class ConversationModel:
    """
    Persistence model for a conversation.
    """

    id: UUID

    user_id: UUID

    status: ConversationStatus

    created_at: datetime

    updated_at: datetime