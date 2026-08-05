from ai_assistant.domain.entities.message import Message

from ..models.message_model import MessageModel


class MessageMapper:
    """
    Maps Message <-> MessageModel
    """

    @staticmethod
    def to_model(
        message: Message,
        conversation_id,
    ) -> MessageModel:

        return MessageModel(
            id=message.id,
            conversation_id=conversation_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )

    @staticmethod
    def to_domain(
        model: MessageModel,
    ) -> Message:

        return Message(
            id=model.id,
            role=model.role,
            content=model.content,
            created_at=model.created_at,
        )