"""
Infrastructure implementation of ConversationRepository.

Responsibilities
----------------
- Persist Conversation aggregates.
- Rehydrate Conversation aggregates.
- Persist child entities (Messages, ToolCalls).
- Delegate object transformation to Mappers.
- Never contain business rules.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ai_assistant.domain.entities.conversation import Conversation
from ai_assistant.domain.repositories.conversation_repository import (
    ConversationRepository,
)

from ..mappers.conversation_mapper import ConversationMapper
from ..mappers.message_mapper import MessageMapper
from ..mappers.tool_call_mapper import ToolCallMapper

from ..models.conversation_model import ConversationModel
from ..models.message_model import MessageModel
from ..models.tool_call_model import ToolCallModel


class PostgresConversationRepository(ConversationRepository):
    """
    PostgreSQL implementation of ConversationRepository.

    Persists Conversation aggregates together with their
    Messages and ToolCalls.

    Business rules belong in the domain, never here.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def save(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Persist the Conversation aggregate.

        Inserts a new aggregate if it does not exist,
        otherwise updates the existing aggregate.

        Child entities are persisted afterwards.
        """

        conversation_exists = await self.exists(
            conversation.id
        )

        if conversation_exists:
            await self._update_conversation(
                conversation
            )
        else:
            await self._insert_conversation(
                conversation
            )

        await self._persist_messages(
            conversation
        )

        await self._persist_tool_calls(
            conversation
        )

    async def exists(
        self,
        conversation_id: UUID,
    ) -> bool:
        """
        Determine whether the aggregate already exists.
        """

        stmt = (
            select(ConversationModel.id)
            .where(
                ConversationModel.id == conversation_id
            )
        )

        result = await self._session.execute(stmt)

        return (
            result.scalar_one_or_none()
            is not None
        )

    # ------------------------------------------------------------------
    # Private Helpers
    # ------------------------------------------------------------------

    async def _insert_conversation(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Insert a new Conversation aggregate.
        """

        model = ConversationMapper.to_model(
            conversation
        )

        self._session.add(model)

        await self._session.flush()

    async def _update_conversation(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Update an existing Conversation aggregate.
        """

        stmt = (
            select(ConversationModel)
            .where(
                ConversationModel.id
                == conversation.id
            )
        )

        result = await self._session.execute(stmt)

        model = result.scalar_one()

        model.status = conversation.status
        model.updated_at = (
            conversation.updated_at
        )

        await self._session.flush()

    async def _persist_messages(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Persist all messages belonging to
        the Conversation aggregate.
        """

        for message in conversation.messages:

            model = MessageMapper.to_model(
                message=message,
                conversation_id=conversation.id,
            )

            await self._session.merge(model)

        await self._session.flush()

    async def _persist_tool_calls(
        self,
        conversation: Conversation,
    ) -> None:
        """
        Persist all tool executions belonging
        to the Conversation aggregate.
        """

        for tool_call in conversation.tool_calls:

            model = ToolCallMapper.to_model(
                tool_call=tool_call,
                conversation_id=conversation.id,
            )

            await self._session.merge(model)

        await self._session.flush()