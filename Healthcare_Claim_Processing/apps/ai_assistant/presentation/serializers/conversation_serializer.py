from uuid import UUID

from pydantic import BaseModel


class ConversationSerializer(BaseModel):
    """
    Request for loading conversation history.
    """

    conversation_id: UUID