
from __future__ import annotations

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
from patient.domain.value_objects.date_of_birth import DateOfBirth
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
    Presentation-layer controller for the Patient bounded context.

    Responsibilities:

        Request Schema
            ↓
        Domain Value Objects
            ↓
        Application Command
            ↓
        Use Case
            ↓
        Response Schema

    The controller does not contain business rules.

    It does not know about:
        - Django
        - HTTP requests
        - SQLAlchemy
        - PostgreSQL
        - transactions
        - Kafka
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

    # =========================================================
    # REGISTER PATIENT
    # =========================================================

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

            name=PatientName(
                first_name=request.first_name,
                last_name=request.last_name,
            ),

            email=Email(
                request.email
            ),

            phone_number=PhoneNumber(
                request.phone_number
            ),

            gender=Gender(
                request.gender
            ),

            date_of_birth=DateOfBirth(
                request.date_of_birth
            ),

            address=Address(
                street=request.street,
                city=request.city,
                state=request.state,
                postal_code=request.postal_code,
                country=request.country,
            ),
        )

        patient = await (
            self._register_patient_use_case.execute(
                command
            )
        )

        return self._to_response(patient)

    # =========================================================
    # UPDATE CONTACT INFORMATION
    # =========================================================

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

            email=Email(
                request.email
            ),

            phone_number=PhoneNumber(
                request.phone_number
            ),

            address=Address(
                street=request.street,
                city=request.city,
                state=request.state,
                postal_code=request.postal_code,
                country=request.country,
            ),
        )

        patient = await (
            self
            ._update_patient_contact_information_use_case
            .execute(command)
        )

        return self._to_response(patient)

    # =========================================================
    # RESPONSE MAPPING
    # =========================================================

    @staticmethod
    def _to_response(
        patient,
    ) -> PatientResponse:
        """
        Convert the Patient domain aggregate into the
        HTTP response schema.

        Domain value objects are deliberately converted
        into primitive HTTP-friendly values here.
        """

        return PatientResponse(
            id=patient.id,

            medical_record_number=str(
                patient.medical_record_number
            ),

            name=str(
                patient.name
            ),

            email=str(
                patient.email
            ),

            phone_number=str(
                patient.phone_number
            ),

            gender=str(
                patient.gender
            ),

            date_of_birth=patient.date_of_birth.value,

            address=str(
                patient.address
            ),

            active=patient.active,
        )
