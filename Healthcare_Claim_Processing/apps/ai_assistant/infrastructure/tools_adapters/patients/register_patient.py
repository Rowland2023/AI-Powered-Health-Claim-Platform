
from __future__ import annotations

from datetime import date
from typing import Any

from .tool import Tool
from ..domain.tool_definition import ToolDefinition
from ..domain.tool_parameter import ToolParameter

from patient.application.commands.register_patient import (
    RegisterPatientCommand,
)
from patient.application.use_cases.register_patient import (
    RegisterPatientUseCase,
)


class RegisterPatientTool(Tool):
    """
    AI tool for registering a new patient.

    This adapter delegates patient registration to the
    Patient bounded context.
    """

    def __init__(
        self,
        register_patient_use_case: RegisterPatientUseCase,
    ) -> None:
        self._register_patient_use_case = (
            register_patient_use_case
        )

    @property
    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name="register_patient",
            description="Register a new patient.",
            parameters=[
                ToolParameter(
                    "medical_record_number",
                    "string",
                    "Patient medical record number",
                ),
                ToolParameter(
                    "name",
                    "string",
                    "Patient full name",
                ),
                ToolParameter(
                    "email",
                    "string",
                    "Patient email address",
                ),
                ToolParameter(
                    "phone_number",
                    "string",
                    "Patient phone number",
                ),
                ToolParameter(
                    "gender",
                    "string",
                    "Patient gender",
                ),
                ToolParameter(
                    "date_of_birth",
                    "date",
                    "Patient date of birth",
                ),
                ToolParameter(
                    "address",
                    "string",
                    "Patient address",
                ),
            ],
        )

    async def execute(
        self,
        **kwargs: Any,
    ):

        date_of_birth = kwargs["date_of_birth"]

        if isinstance(date_of_birth, str):
            date_of_birth = date.fromisoformat(
                date_of_birth
            )

        command = RegisterPatientCommand(
            medical_record_number=kwargs[
                "medical_record_number"
            ],
            name=kwargs["name"],
            email=kwargs["email"],
            phone_number=kwargs["phone_number"],
            gender=kwargs["gender"],
            date_of_birth=date_of_birth,
            address=kwargs["address"],
        )

        return await self._register_patient_use_case.execute(
            command
        )
