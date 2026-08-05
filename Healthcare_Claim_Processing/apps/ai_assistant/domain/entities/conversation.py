from __future__ import annotations

from datetime import datetime
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
        self._created_at = created_at or datetime.utcnow()

    @classmethod
    def start(
        cls,
        user_id: UUID,
    ) -> "Conversation":

        conversation = cls(
            id=uuid4(),
            user_id=user_id,
        )

        conversation.record_event(
            ConversationStarted(
                conversation.id,
                user_id,
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

        self.record_event(
            UserMessageAdded(
                self.id,
                message.id,
            )
        )

        return message

    def add_assistant_message(
        self,
        content: str,
    ) -> Message:

        message = Message.assistant(content)

        self._messages.append(message)

        self.record_event(
            AssistantMessageAdded(
                self.id,
                message.id,
            )
        )

        return message