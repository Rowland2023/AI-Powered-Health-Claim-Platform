from abc import ABC, abstractmethod
from uuid import UUID

from ..entities.conversation import Conversation


class ConversationRepository(ABC):
    """
    Repository for Conversation aggregates.
    """

    @abstractmethod
    async def save(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Persist a conversation aggregate.
        """

    @abstractmethod
    async def find_by_id(
        self,
        conversation_id: UUID,
    ) -> Conversation | None:
        """
        Retrieve a conversation by its identifier.
        """

    @abstractmethod
    async def find_active_by_user(
        self,
        user_id: UUID,
    ) -> Conversation | None:
        """
        Retrieve the active conversation for a user.
        """

    @abstractmethod
    async def delete(
        self,
        conversation_id: UUID,
    ) -> None:
        """
        Remove or archive a conversation.
        """