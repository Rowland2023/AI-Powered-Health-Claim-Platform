
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

from shared.infrastructure.database.session import (
    SessionFactory,
)


def create_patient_dependencies() -> dict:
    """
    Build and wire the Patient module dependencies.

    Composition root responsibilities:

        Infrastructure
            ↓
        UnitOfWork
            ↓
        Application use cases
            ↓
        Presentation

    The application layer does not construct infrastructure
    implementations itself.
    """

    register_patient_uow = SQLAlchemyUnitOfWork(
        session_factory=SessionFactory,
    )

    update_patient_contact_uow = SQLAlchemyUnitOfWork(
        session_factory=SessionFactory,
    )

    register_patient_use_case = RegisterPatientUseCase(
        uow=register_patient_uow,
    )

    update_patient_contact_information_use_case = (
        UpdatePatientContactInformationUseCase(
            uow=update_patient_contact_uow,
        )
    )

    return {
        "register_patient_use_case": register_patient_use_case,
        "update_patient_contact_information_use_case": (
            update_patient_contact_information_use_case
        ),
    }
