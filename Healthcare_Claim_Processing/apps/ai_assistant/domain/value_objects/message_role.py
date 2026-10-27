from enum import Enum


class MessageRole(str, Enum):
    """
    Role of a message within a conversation.
    """

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"

    TOOL = "tool"