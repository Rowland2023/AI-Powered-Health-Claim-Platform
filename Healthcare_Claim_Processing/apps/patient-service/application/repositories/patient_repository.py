
from __future__ import annotations

from abc import ABC, abstractmethod

from uuid import UUID

from patient.domain.entities.patient import Patient
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)


class PatientRepository(ABC):
    """
    Application-facing repository port for the Patient aggregate.

    The application/domain layers depend on this abstraction.

    Infrastructure provides the concrete implementation.

    The application layer does not know:
        - SQLAlchemy
        - PostgreSQL
        - SQL queries
        - database sessions
        - table names
    """

    @abstractmethod
    async def get_by_id(
        self,
        patient_id: UUID,
    ) -> Patient | None:
        """
        Retrieve a patient by its aggregate ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_medical_record_number(
        self,
        medical_record_number: MedicalRecordNumber,
    ) -> Patient | None:
        """
        Retrieve a patient by medical record number.
        """
        raise NotImplementedError

    @abstractmethod
    async def add(
        self,
        patient: Patient,
    ) -> None:
        """
        Persist a newly created Patient aggregate.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        patient: Patient,
    ) -> None:
        """
        Persist changes to an existing Patient aggregate.
        """
        raise NotImplementedError
