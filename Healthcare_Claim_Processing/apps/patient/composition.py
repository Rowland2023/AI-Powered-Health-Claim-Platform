from __future__ import annotations

from patient.application.use_cases.register_patient import (
    RegisterPatientUseCase,
)
from patient.application.use_cases.update_patient_contact_information import (
    UpdatePatientContactInformationUseCase,
)
from patient.infrastructure.persistence.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)
from patient.presentation.http.controllers.patient_controller import (
    PatientController,
)
from shared.infrastructure.database.session import SessionFactory


def create_patient_uow() -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(
        session_factory=SessionFactory,
    )


def create_patient_dependencies() -> dict:
    """
    Compose all Patient bounded-context dependencies.
    """

    register_patient_use_case = RegisterPatientUseCase(
        uow=create_patient_uow(),
    )

    update_patient_contact_information_use_case = (
        UpdatePatientContactInformationUseCase(
            uow=create_patient_uow(),
        )
    )

    patient_controller = PatientController(
        register_patient_use_case=register_patient_use_case,
        update_patient_contact_information_use_case=(
            update_patient_contact_information_use_case
        ),
    )

    return {
        "register_patient_use_case": register_patient_use_case,
        "update_patient_contact_information_use_case": (
            update_patient_contact_information_use_case
        ),
        "patient_controller": patient_controller,
    }