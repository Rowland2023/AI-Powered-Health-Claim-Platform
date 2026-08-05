from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class GetConversationHistoryQuery:

    conversation_id: UUID