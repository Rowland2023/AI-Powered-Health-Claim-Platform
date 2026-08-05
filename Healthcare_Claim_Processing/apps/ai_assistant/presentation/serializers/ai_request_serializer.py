from uuid import UUID

from pydantic import BaseModel, Field


class AIRequestSerializer(BaseModel):
    """
    Validates an incoming AI chat request.
    """

    prompt: str = Field(
        min_length=1,
        max_length=8000,
    )

    conversation_id: UUID | None = None

    temperature: float = Field(
        default=0.2,
        ge=0,
        le=2,
    )

    max_tokens: int = Field(
        default=1024,
        gt=0,
        le=4096,
    )