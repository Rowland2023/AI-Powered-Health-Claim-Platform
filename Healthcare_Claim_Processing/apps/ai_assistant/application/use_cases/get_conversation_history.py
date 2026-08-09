
from __future__ import annotations

from uuid import UUID

from shared.application.result import Result

from ai_assistant.application.services.conversation_service import (
    ConversationService,
)


class GetConversationHistoryUseCase:
    """
    Application use case for retrieving conversation history.

    The use case coordinates the application operation while
    ConversationService provides the persistence capability.
    """

    def __init__(
        self,
        conversation_service: ConversationService,
    ) -> None:
        self._conversation_service = conversation_service

    async def execute(
        self,
        conversation_id: UUID,
    ) -> Result[list[dict]]:
        """
        Retrieve all messages belonging to a conversation.
        """

        history = await self._conversation_service.get_history(
            conversation_id
        )

        return Result.success(history)
