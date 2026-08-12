from __future__ import annotations

import json
from json import JSONDecodeError
from uuid import UUID

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

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


def create_patient_views(
    register_patient_use_case: RegisterPatientUseCase,
    update_patient_contact_information_use_case: (
        UpdatePatientContactInformationUseCase
    ),
):
    """
    Create Django HTTP views with application use cases
    already composed.

    The view is responsible for:

        HTTP request
            ↓
        Request schema
            ↓
        Application command
            ↓
        Use case
            ↓
        Response schema
            ↓
        HTTP response
    """

    @require_http_methods(["POST"])
    async def register_patient(request):
        try:
            payload = json.loads(
                request.body.decode("utf-8")
            )

            schema = RegisterPatientRequest.model_validate(
                payload
            )

        except JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON payload."},
                status=400,
            )

        except ValueError as exc:
            return JsonResponse(
                {"error": str(exc)},
                status=400,
            )

        command = RegisterPatientCommand(
            medical_record_number=MedicalRecordNumber(
                schema.medical_record_number
            ),
            name=PatientName(
                first_name=schema.first_name,
                last_name=schema.last_name,
            ),
            email=Email(schema.email),
            phone_number=PhoneNumber(
                schema.phone_number
            ),
            gender=Gender(schema.gender),
            date_of_birth=DateOfBirth(
                schema.date_of_birth
            ),
            address=Address(
                street=schema.street,
                city=schema.city,
                state=schema.state,
                postal_code=schema.postal_code,
                country=schema.country,
            ),
        )

        patient = await register_patient_use_case.execute(
            command
        )

        response = PatientResponse(
            id=patient.id,
            medical_record_number=str(
                patient.medical_record_number
            ),
            name=str(patient.name),
            email=str(patient.email),
            phone_number=str(patient.phone_number),
            gender=str(patient.gender),
            date_of_birth=patient.date_of_birth.value,
            address=str(patient.address),
            active=patient.active,
        )

        return JsonResponse(
            response.model_dump(mode="json"),
            status=201,
        )

    @require_http_methods(["PATCH"])
    async def update_patient_contact_information(
        request,
        patient_id: UUID,
    ):
        try:
            payload = json.loads(
                request.body.decode("utf-8")
            )

            schema = (
                UpdatePatientContactInformationRequest
                .model_validate(payload)
            )

        except JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON payload."},
                status=400,
            )

        except ValueError as exc:
            return JsonResponse(
                {"error": str(exc)},
                status=400,
            )

        command = UpdatePatientContactInformationCommand(
            patient_id=patient_id,
            email=Email(schema.email),
            phone_number=PhoneNumber(
                schema.phone_number
            ),
            address=Address(
                street=schema.street,
                city=schema.city,
                state=schema.state,
                postal_code=schema.postal_code,
                country=schema.country,
            ),
        )

        patient = (
            await update_patient_contact_information_use_case.execute(
                command
            )
        )

        response = PatientResponse(
            id=patient.id,
            medical_record_number=str(
                patient.medical_record_number
            ),
            name=str(patient.name),
            email=str(patient.email),
            phone_number=str(patient.phone_number),
            gender=str(patient.gender),
            date_of_birth=patient.date_of_birth.value,
            address=str(patient.address),
            active=patient.active,
        )

        return JsonResponse(
            response.model_dump(mode="json"),
            status=200,
        )

    return (
        register_patient,
        update_patient_contact_information,
    )