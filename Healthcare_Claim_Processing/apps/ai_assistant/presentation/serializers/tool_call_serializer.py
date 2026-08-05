from typing import Any

from pydantic import BaseModel


class ToolCallSerializer(BaseModel):
    """
    Validates manual tool execution requests.
    """

    tool_name: str

    arguments: dict[str, Any]