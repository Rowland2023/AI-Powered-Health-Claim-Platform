from abc import ABC, abstractmethod
from typing import Sequence
from uuid import UUID

from ai_assistant.domain.entities.conversation import Conversation
from ai_assistant.domain.entities.message import Message


class ConversationRepository(ABC):
    """
    Repository contract for persisting AI conversations and messages.
    """

    @abstractmethod
    async def save(self, conversation: Conversation) -> None:
        """
        Persist a conversation aggregate.
        """
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        """
        Retrieve a conversation aggregate.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists(
        self,
        conversation_id: UUID,
    ) -> bool:
        """
        Check whether a conversation exists.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(
        self,
        conversation_id: UUID,
    ) -> None:
        """
        Soft delete or archive a conversation.
        """
        raise NotImplementedError

    @abstractmethod
    async def append_message(
        self,
        conversation_id: UUID,
        message: Message,
    ) -> None:
        """
        Append a new message to an existing conversation.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_messages(
        self,
        conversation_id: UUID,
    ) -> Sequence[Message]:
        """
        Return the complete conversation history.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_recent_messages(
        self,
        conversation_id: UUID,
        limit: int = 20,
    ) -> Sequence[Message]:
        """
        Return the most recent messages.
        """
        raise NotImplementedError