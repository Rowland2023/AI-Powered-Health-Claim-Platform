from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ai_assistant.domain.value_objects.tool_execution_status import (
    ToolExecutionStatus,
)


@dataclass(slots=True)
class ToolCallModel:
    """
    Persistence model for executed tool calls.
    """

    id: UUID

    conversation_id: UUID

    tool_name: str

    arguments_json: str

    result_json: str | None

    status: ToolExecutionStatus

    created_at: datetime

    executed_at: datetime | None