
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

        model.name = patient.name.value
        model.email = patient.email.value
        model.phone_number = patient.phone_number.value
        model.gender = patient.gender.value
        model.date_of_birth = patient.date_of_birth.value
        model.address = patient.address.value
        model.active = patient.active
        model.created_at = patient.created_at
        model.updated_at = patient.updated_at

        # -----------------------------------------------------
        # Insurance policy
        # -----------------------------------------------------

        if patient.insurance_policy is None:
            model.insurance_policy = None

        else:
            if model.insurance_policy is None:
                model.insurance_policy = (
                    PatientMapper._insurance_policy_to_model(
                        patient.insurance_policy,
                        patient.id,
                    )
                )

            else:
                policy_model = model.insurance_policy
                policy = patient.insurance_policy

                policy_model.id = policy.id
                policy_model.insurance_number = (
                    policy.insurance_number.value
                )
                policy_model.provider = policy.provider
                policy_model.policy_type = policy.policy_type
                policy_model.effective_date = (
                    policy.effective_date
                )
                policy_model.expiry_date = policy.expiry_date
                policy_model.status = policy.status.value

        # -----------------------------------------------------
        # Emergency contacts
        # -----------------------------------------------------
        #
        # Because the aggregate owns the collection and there
        # is currently no separate contact repository, we
        # synchronize the child collection here.
        #

        existing_contacts = {
            contact.id: contact
            for contact in model.emergency_contacts
        }

        incoming_contacts = {
            contact.id: contact
            for contact in patient.emergency_contacts
        }

        # Remove contacts that no longer belong to the aggregate.
        model.emergency_contacts = [
            contact_model
            for contact_id, contact_model in existing_contacts.items()
            if contact_id in incoming_contacts
        ]

        # Update existing contacts and add new ones.
        existing_by_id = {
            contact.id: contact
            for contact in model.emergency_contacts
        }

        for contact in patient.emergency_contacts:

            existing = existing_by_id.get(contact.id)

            if existing is None:
                model.emergency_contacts.append(
                    PatientMapper._emergency_contact_to_model(
                        contact,
                        patient.id,
                    )
                )
                continue

            existing.name = contact.name.value
            existing.phone_number = contact.phone_number.value
            existing.relationship = contact.relationship
            existing.email = (
                contact.email.value
                if contact.email is not None
                else None
            )
