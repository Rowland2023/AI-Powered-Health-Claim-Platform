
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status

from patient.presentation.http.controllers.patient_controller import (
    PatientController,
)

from patient.presentation.http.schemas.patient_schema import (
    PatientResponse,
    RegisterPatientRequest,
    UpdatePatientContactInformationRequest,
)


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


def get_patient_controller() -> PatientController:
    """
    Dependency injection boundary.

    The application bootstrap/composition root should replace or
    configure this dependency with the actual controller instance.

    This function intentionally does not construct repositories,
    sessions, or use cases.
    """

    raise NotImplementedError(
        "PatientController dependency has not been configured."
    )


@router.post(
    "",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_patient(
    request: RegisterPatientRequest,
    controller: PatientController = Depends(
        get_patient_controller
    ),
) -> PatientResponse:
    """
    Register a patient.
    """

    return await controller.register_patient(request)


@router.patch(
    "/{patient_id}/contact-information",
    response_model=PatientResponse,
    status_code=status.HTTP_200_OK,
)
async def update_contact_information(
    patient_id: UUID,
    request: UpdatePatientContactInformationRequest,
    controller: PatientController = Depends(
        get_patient_controller
    ),
) -> PatientResponse:
    """
    Update patient contact information.
    """

    return await controller.update_contact_information(
        patient_id=patient_id,
        request=request,
    )
