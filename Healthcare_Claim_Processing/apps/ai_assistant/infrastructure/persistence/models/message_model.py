from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ai_assistant.domain.value_objects.message_role import MessageRole


@dataclass(slots=True)
class MessageModel:
    """
    Persistence model for conversation messages.
    """

    id: UUID

    conversation_id: UUID

    role: MessageRole

    content: str

    created_at: datetime