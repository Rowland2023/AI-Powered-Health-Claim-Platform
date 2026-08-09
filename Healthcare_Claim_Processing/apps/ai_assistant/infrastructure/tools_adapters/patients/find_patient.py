
from __future__ import annotations

from typing import Any

from .tool import Tool
from ..domain.tool_definition import ToolDefinition
from ..domain.tool_parameter import ToolParameter


class FindPatientTool(Tool):
    """
    AI tool for finding an existing patient.

    Patient lookup is delegated to the Patient bounded
    context's application layer.
    """

    def __init__(
        self,
        find_patient_use_case,
    ) -> None:
        self._find_patient_use_case = find_patient_use_case

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="find_patient",
            description="Find an existing patient.",
            parameters=[
                ToolParameter(
                    "patient_identifier",
                    "string",
                    "Patient ID, medical record number, email, or phone number",
                ),
            ],
        )

    async def execute(
        self,
        **kwargs: Any,
    ):
        return await self._find_patient_use_case.execute(
            kwargs["patient_identifier"]
        )
