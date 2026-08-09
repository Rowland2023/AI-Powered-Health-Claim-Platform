
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from patient.domain.entities.patient import Patient
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)


class PatientRepository(ABC):
    """
    Repository port for the Patient aggregate.

    This is a domain/application-facing abstraction.
    Infrastructure provides the concrete implementation.
    """

    @abstractmethod
    async def add(
        self,
        patient: Patient,
    ) -> None:
        """
        Persist a newly registered patient.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(
        self,
        patient_id: UUID,
    ) -> Optional[Patient]:
        """
        Retrieve a patient by aggregate ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_medical_record_number(
        self,
        medical_record_number: MedicalRecordNumber,
    ) -> Optional[Patient]:
        """
        Retrieve a patient using the medical record number.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists_by_medical_record_number(
        self,
        medical_record_number: MedicalRecordNumber,
    ) -> bool:
        """
        Determine whether a medical record number is already assigned.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(
        self,
        patient: Patient,
    ) -> None:
        """
        Persist changes to an existing patient aggregate.
        """
        raise NotImplementedError
