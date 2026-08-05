from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID, uuid4

from ..value_objects.message_role import MessageRole


@dataclass(slots=True)
class Message:
    """
    Entity representing a single message within an AI conversation.
    """

    id: UUID
    role: MessageRole
    content: str
    created_at: datetime

    @classmethod
    def user(cls, content: str) -> "Message":
        return cls(
            id=uuid4(),
            role=MessageRole.USER,
            content=content,
            created_at=datetime.now(UTC),
        )

    @classmethod
    def assistant(cls, content: str) -> "Message":
        return cls(
            id=uuid4(),
            role=MessageRole.ASSISTANT,
            content=content,
            created_at=datetime.now(UTC),
        )

    @classmethod
    def system(cls, content: str) -> "Message":
        return cls(
            id=uuid4(),
            role=MessageRole.SYSTEM,
            content=content,
            created_at=datetime.now(UTC),
        )

    @classmethod
    def tool(
        cls,
        content: str,
    ) -> "Message":
        return cls(
            id=uuid4(),
            role=MessageRole.TOOL,
            content=content,
            created_at=datetime.now(UTC),
        )