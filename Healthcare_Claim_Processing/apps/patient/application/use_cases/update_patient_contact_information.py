
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from patient.application.unit_of_work import UnitOfWork

from patient.domain.entities.patient import Patient
from patient.domain.value_objects.address import Address
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.phone_number import PhoneNumber


@dataclass(frozen=True)
class UpdatePatientContactInformationCommand:
    """
    Data required to update a patient's contact information.
    """

    patient_id: UUID
    email: Email
    phone_number: PhoneNumber
    address: Address


class UpdatePatientContactInformationUseCase:
    """
    Application use case for updating patient contact information.

    The use case orchestrates the operation.

    The Patient aggregate owns the actual business behavior.
    """

    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self._uow = uow

    async def execute(
        self,
        command: UpdatePatientContactInformationCommand,
    ) -> Patient:

        async with self._uow as uow:

            # -------------------------------------------------
            # 1. Load aggregate
            # -------------------------------------------------

            patient = await (
                uow.patient_repository
                .get_by_id(command.patient_id)
            )

            if patient is None:
                raise ValueError(
                    f"Patient {command.patient_id} was not found."
                )

            # -------------------------------------------------
            # 2. Ask aggregate to perform the business change
            # -------------------------------------------------

            patient.update_contact_information(
                email=command.email,
                phone_number=command.phone_number,
                address=command.address,
            )

            # -------------------------------------------------
            # 3. Persist aggregate
            # -------------------------------------------------

            await uow.patient_repository.update(patient)

            # -------------------------------------------------
            # 4. Register aggregate with UoW
            # -------------------------------------------------

            uow.register(patient)

            # -------------------------------------------------
            # 5. Commit aggregate + domain events atomically
            # -------------------------------------------------

            await uow.commit()

            return patient
