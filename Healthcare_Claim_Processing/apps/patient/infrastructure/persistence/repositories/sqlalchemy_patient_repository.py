
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from patient.application.repositories.patient_repository import (
    PatientRepository,
)
from patient.domain.entities.patient import Patient
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)

from patient.infrastructure.persistence.mappers.patient_mapper import (
    PatientMapper,
)
from patient.infrastructure.persistence.models.patient_model import (
    PatientModel,
)


class SQLAlchemyPatientRepository(PatientRepository):
    """
    SQLAlchemy implementation of the PatientRepository port.

    This class belongs entirely to infrastructure.

    The application layer knows only about PatientRepository.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    # =========================================================
    # READ
    # =========================================================

    async def get_by_id(
        self,
        patient_id: UUID,
    ) -> Patient | None:
        """
        Retrieve a complete Patient aggregate by ID.
        """

        statement = (
            select(PatientModel)
            .where(PatientModel.id == patient_id)
            .options(
                selectinload(PatientModel.insurance_policy),
                selectinload(PatientModel.emergency_contacts),
            )
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return PatientMapper.to_domain(model)

    async def get_by_medical_record_number(
        self,
        medical_record_number: MedicalRecordNumber,
    ) -> Patient | None:
        """
        Retrieve a complete Patient aggregate by medical
        record number.
        """

        statement = (
            select(PatientModel)
            .where(
                PatientModel.medical_record_number
                == medical_record_number.value
            )
            .options(
                selectinload(PatientModel.insurance_policy),
                selectinload(PatientModel.emergency_contacts),
            )
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return PatientMapper.to_domain(model)

    # =========================================================
    # CREATE
    # =========================================================

    async def add(
        self,
        patient: Patient,
    ) -> None:
        """
        Add a new Patient aggregate to the current transaction.

        No commit occurs here.

        The UnitOfWork owns transaction completion.
        """

        model = PatientMapper.to_model(patient)

        self._session.add(model)

    # =========================================================
    # UPDATE
    # =========================================================

    async def update(
        self,
        patient: Patient,
    ) -> None:
        """
        Update an existing Patient aggregate.

        The existing persistence graph is loaded into the current
        session and mutated rather than inserting a new graph.
        """

        statement = (
            select(PatientModel)
            .where(PatientModel.id == patient.id)
            .options(
                selectinload(PatientModel.insurance_policy),
                selectinload(PatientModel.emergency_contacts),
            )
        )

        result = await self._session.execute(statement)

        model = result.scalar_one_or_none()

        if model is None:
            raise ValueError(
                f"Patient {patient.id} was not found."
            )

        # -----------------------------------------------------
        # Patient fields
        # -----------------------------------------------------

        model.medical_record_number = (
            patient.medical_record_number.value
        )

        model.first_name = patient.name.first_name
        model.last_name = patient.name.last_name

        model.email = patient.email.value
        model.phone_number = patient.phone_number.value
        model.gender = patient.gender.value
        model.date_of_birth = patient.date_of_birth.value

        # -----------------------------------------------------
        # Address
        # -----------------------------------------------------

        model.street = patient.address.street
        model.city = patient.address.city
        model.state = patient.address.state
        model.postal_code = patient.address.postal_code
        model.country = patient.address.country

        # -----------------------------------------------------
        # Status and timestamps
        # -----------------------------------------------------

        model.active = patient.active
        model.created_at = patient.created_at
        model.updated_at = patient.updated_at
