from __future__ import annotations

import json
from json import JSONDecodeError
from uuid import UUID

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from patient.presentation.http.controllers.patient_controller import (
    PatientController,
)

from patient.presentation.http.schemas.patient_schema import (
    RegisterPatientRequest,
    UpdatePatientContactInformationRequest,
)


def create_patient_views(
    controller: PatientController,
):
    """
    Create Django HTTP views with the Patient controller
    already composed.
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

        except Exception as exc:
            return JsonResponse(
                {"error": str(exc)},
                status=400,
            )

        patient = await controller.register_patient(
            schema
        )

        return JsonResponse(
            patient.model_dump(mode="json"),
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

        except Exception as exc:
            return JsonResponse(
                {"error": str(exc)},
                status=400,
            )

        patient = (
            await controller.update_contact_information(
                patient_id,
                schema,
            )
        )

        return JsonResponse(
            patient.model_dump(mode="json"),
            status=200,
        )

    return (
        register_patient,
        update_patient_contact_information,
    )