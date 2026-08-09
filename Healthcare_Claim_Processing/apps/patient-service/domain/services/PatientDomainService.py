### `patient/domain/services/PatientDomainService.py`


from __future__ import annotations

from uuid import UUID

from ..entities.Patient import Patient


class PatientDomainService:
    """
    Domain service containing business rules that do not naturally
    belong to the Patient aggregate itself.

    This service must remain independent of:
        - FastAPI
        - SQLAlchemy
        - Kafka
        - repositories
        - UnitOfWork
        - HTTP
    """

    @staticmethod
    def can_be_deactivated(
        patient: Patient,
    ) -> bool:
        """
        Determine whether the patient can be deactivated.

        The actual policy can become richer as the domain evolves.
        """

        return patient.active

    @staticmethod
    def has_active_insurance(
        patient: Patient,
    ) -> bool:
        """
        Determine whether the patient currently has an insurance
        policy associated with the aggregate.
        """

        return patient.insurance_policy is not None

    @staticmethod
    def belongs_to_patient(
        patient: Patient,
        patient_id: UUID,
    ) -> bool:
        """
        Domain helper for determining aggregate identity.
        """

        return patient.id == patient_id
