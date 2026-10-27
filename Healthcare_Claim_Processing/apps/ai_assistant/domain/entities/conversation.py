from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from shared.domain.aggregate_root import AggregateRoot

from ..events.conversation_started import ConversationStarted
from ..events.user_message_added import UserMessageAdded
from ..events.assistant_message_added import AssistantMessageAdded

from .message import Message


class Conversation(AggregateRoot):
    """
    Aggregate Root representing a conversation between
    a user and the AI assistant.
    """

    def __init__(
        self,
        id: UUID,
        user_id: UUID,
        messages: list[Message] | None = None,
        created_at: datetime | None = None,
    ):

        super().__init__()

        self._id = id
        self._user_id = user_id
        self._messages = messages or []
        self._created_at = created_at or datetime.now(timezone.utc)

    @classmethod
    def start(
        cls,
        user_id: UUID,
    ) -> "Conversation":

        conversation = cls(
            id=uuid4(),
            user_id=user_id,
        )

        conversation.add_domain_event(
            ConversationStarted(
                conversation_id=conversation.id,
                user_id=user_id,
                aggregate_id=conversation.id,
            )
        )

        return conversation

    @property
    def id(self):

        return self._id

    @property
    def user_id(self):

        return self._user_id

    @property
    def messages(self):

        return tuple(self._messages)

    def add_user_message(
        self,
        content: str,
    ) -> Message:

        message = Message.user(content)

        self._messages.append(message)

        self.add_domain_event(
            UserMessageAdded(
                conversation_id=self.id,
                message_id=message.id,
                aggregate_id=self.id,
            )
        )

        return message

    def add_assistant_message(
        self,
        content: str,
    ) -> Message:

        message = Message.assistant(content)

        self._messages.append(message)

        self.add_domain_event(
            AssistantMessageAdded(
                conversation_id=self.id,
                message_id=message.id,
                aggregate_id=self.id,
            )
        )

        return message