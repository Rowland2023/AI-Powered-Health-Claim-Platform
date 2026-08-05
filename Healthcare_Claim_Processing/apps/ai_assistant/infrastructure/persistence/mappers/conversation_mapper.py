from ai_assistant.domain.entities.conversation import Conversation

from .message_mapper import MessageMapper
from .tool_call_mapper import ToolCallMapper

from ..models.conversation_model import ConversationModel


class ConversationMapper:

    @staticmethod
    def to_model(
        conversation: Conversation,
    ) -> ConversationModel:

        return ConversationModel(
            id=conversation.id,
            user_id=conversation.user_id,
            status=conversation.status,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )

    @staticmethod
    def to_domain(
        model: ConversationModel,
        messages,
        tool_calls,
    ) -> Conversation:

        return Conversation(
            id=model.id,
            user_id=model.user_id,
            status=model.status,
            messages=[
                MessageMapper.to_domain(m)
                for m in messages
            ],
            tool_calls=[
                ToolCallMapper.to_domain(t)
                for t in tool_calls
            ],
            created_at=model.created_at,
            updated_at=model.updated_at,
        )