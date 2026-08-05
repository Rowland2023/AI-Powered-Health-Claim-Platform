from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class AIRequest:

    user_id: UUID

    prompt: str

    request_id: UUID = field(
        default_factory=uuid4
    )

    conversation_id: UUID | None = None

    def validate(self):

        if not self.prompt.strip():

            raise ValueError(
                "Prompt cannot be empty."
            )