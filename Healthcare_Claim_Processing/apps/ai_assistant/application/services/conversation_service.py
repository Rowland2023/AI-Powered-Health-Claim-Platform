# ai_assistant/application/services/conversation_service.py

from abc import ABC, abstractmethod
from uuid import UUID


class ConversationService(ABC):
    """
    Port for conversation persistence.

    Implementations may use PostgreSQL,
    Redis, MongoDB, etc.
    """

    @abstractmethod
    async def get_history(
        self,
        conversation_id: UUID,
    ) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def save_message(
        self,
        conversation_id: UUID,
        role: str,
        content: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_history(
        self,
        conversation_id: UUID,
    ) -> None:
        raise NotImplementedError