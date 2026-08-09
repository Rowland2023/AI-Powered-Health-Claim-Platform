
from __future__ import annotations

from patient.application.commands.register_patient import (
    RegisterPatientCommand,
)
from patient.application.unit_of_work import UnitOfWork
from patient.domain.entities.patient import Patient


class RegisterPatientUseCase:
    """
    Application use case for registering a patient.

    Coordinates:
        Command
            ↓
        Patient aggregate
            ↓
        Patient repository
            ↓
        Unit of Work
            ↓
        Transactional Outbox

    The use case does not know how PostgreSQL, Kafka, or the
    outbox are implemented.
    """

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
        self,
        command: RegisterPatientCommand,
    ) -> Patient:

        async with self._uow as uow:

            # -------------------------------------------------
            # 1. Application-level uniqueness check
            # -------------------------------------------------

            existing_patient = (
                await uow.patient_repository.get_by_medical_record_number(
                    command.medical_record_number
                )
            )

            if existing_patient is not None:
                raise ValueError(
                    "A patient with this medical record number "
                    "already exists."
                )

            # -------------------------------------------------
            # 2. Let the domain create the aggregate
            # -------------------------------------------------

            patient = Patient.register(
                medical_record_number=command.medical_record_number,
                name=command.name,
                email=command.email,
                phone_number=command.phone_number,
                gender=command.gender,
                date_of_birth=command.date_of_birth,
                address=command.address,
            )

            # -------------------------------------------------
            # 3. Persist aggregate
            # -------------------------------------------------

            await uow.patient_repository.add(patient)

            # -------------------------------------------------
            # 4. Register aggregate with Unit of Work
            # -------------------------------------------------

            uow.register(patient)

            # -------------------------------------------------
            # 5. Atomic commit
            #
            #    Patient state
            #         +
            #    Domain events → Outbox
            #         ↓
            #       COMMIT
            # -------------------------------------------------

            await uow.commit()

            return patient
