from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class ExecutePromptCommand:
    """
    Command used to submit a natural language prompt.
    """

    prompt: str

    user_id: UUID

    conversation_id: Optional[UUID] = None

    temperature: float = 0.2

    max_tokens: int = 1024