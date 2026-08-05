from abc import ABC, abstractmethod
from typing import Any

from .tool_definition import ToolDefinition


class Tool(ABC):
    """
    Base class for every AI tool.

    Each Tool delegates work to an Application Use Case.
    """

    @property
    @abstractmethod
    def definition(self) -> ToolDefinition:
        ...

    @abstractmethod
    async def execute(
        self,
        **kwargs: Any,
    ) -> Any:
        ...