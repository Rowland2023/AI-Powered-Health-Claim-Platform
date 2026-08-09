
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .tool_definition import ToolDefinition


class Tool(ABC):
    """
    Base class for every AI tool.

    Each tool exposes a ToolDefinition and delegates its
    actual work to an application use case.
    """

    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        """
        Public definition consumed by the AI assistant.
        """
        ...

    @abstractmethod
    async def execute(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Execute the tool.
        """
        ...
