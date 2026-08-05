from typing import Any

from pydantic import BaseModel


class ToolResultSerializer(BaseModel):

    success: bool

    message: str | None = None

    data: dict[str, Any] | None = None

    error: str | None = None