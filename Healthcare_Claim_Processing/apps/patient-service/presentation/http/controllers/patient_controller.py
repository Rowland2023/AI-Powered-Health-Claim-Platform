
from __future__ import annotations

from datetime import date
from uuid import UUID

from patient.application.commands.register_patient import (
    RegisterPatientCommand,
)
from patient.application.use_cases.register_patient import (
    RegisterPatientUseCase,
)
from patient.application.use_cases.update_patient_contact_information import (
    UpdatePatientContactInformationCommand,
    UpdatePatientContactInformationUseCase,
)

from patient.domain.value_objects.address import Address
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber

from patient.presentation.http.schemas.patient_schema import (
    PatientResponse,
    RegisterPatientRequest,
    UpdatePatientContactInformationRequest,
)


class PatientController:
    """
    Thin HTTP adapter for Patient use cases.

    Responsibilities:
        HTTP request
            ↓
        validate / extract input
            ↓
        construct application command
            ↓
        execute use case
            ↓
        transform domain result into HTTP response

    No business rules live here.
    """

    def __init__(
        self,
        register_patient_use_case: RegisterPatientUseCase,
        update_patient_contact_information_use_case: (
            UpdatePatientContactInformationUseCase
        ),
    ) -> None:
        self._register_patient_use_case = (
            register_patient_use_case
        )

        self._update_patient_contact_information_use_case = (
            update_patient_contact_information_use_case
        )

    async def register_patient(
        self,
        request: RegisterPatientRequest,
    ) -> PatientResponse:
        """
        Register a new patient.
        """

        command = RegisterPatientCommand(
            medical_record_number=MedicalRecordNumber(
                request.medical_record_number
            ),
            name=PatientName(request.name),
            email=Email(request.email),
            phone_number=PhoneNumber(request.phone_number),
            gender=Gender(request.gender),
            date_of_birth=request.date_of_birth,
            address=Address(request.address),
        )

        patient = await self._register_patient_use_case.execute(
            command
        )

        return self._to_response(patient)

    async def update_contact_information(
        self,
        patient_id: UUID,
        request: UpdatePatientContactInformationRequest,
    ) -> PatientResponse:
        """
        Update patient contact information.
        """

        command = UpdatePatientContactInformationCommand(
            patient_id=patient_id,
            email=Email(request.email),
            phone_number=PhoneNumber(request.phone_number),
            address=Address(request.address),
        )

        patient = (
            await self._update_patient_contact_information_use_case
            .execute(command)
        )

        return self._to_response(patient)

    @staticmethod
    def _to_response(patient) -> PatientResponse:
        """
        Convert the domain aggregate into an HTTP response DTO.
        """

        return PatientResponse(
            id=patient.id,
            medical_record_number=str(
                patient.medical_record_number
            ),
            name=str(patient.name),
            email=str(patient.email),
            phone_number=str(patient.phone_number),
            gender=str(patient.gender),
            date_of_birth=(
                patient.date_of_birth.value
                if hasattr(patient.date_of_birth, "value")
                else patient.date_of_birth
            ),
            address=str(patient.address),
            active=patient.active,
            created_at=patient.created_at.isoformat(),
            updated_at=patient.updated_at.isoformat(),
        )
