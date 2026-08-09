
from __future__ import annotations

from patient.domain.entities.emergency_contact import EmergencyContact
from patient.domain.entities.insurance_policy import (
    InsurancePolicy,
    InsurancePolicyStatus,
)
from patient.domain.entities.patient import Patient

from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber

from patient.infrastructure.persistence.models.emergency_contact_model import (
    EmergencyContactModel,
)
from patient.infrastructure.persistence.models.insurance_policy_model import (
    InsurancePolicyModel,
)
from patient.infrastructure.persistence.models.patient_model import (
    PatientModel,
)


class PatientMapper:
    """
    Maps between the Patient domain aggregate and SQLAlchemy
    persistence models.

    The mapper is the boundary between:

        Domain
            ↓
        Persistence

    It prevents SQLAlchemy concerns from leaking into the
    domain model.
    """

    # =========================================================
    # MODEL → DOMAIN
    # =========================================================

    @staticmethod
    def to_domain(model: PatientModel) -> Patient:
        """
        Reconstruct a complete Patient aggregate from persistence.
        """

        insurance_policy = None

        if model.insurance_policy is not None:
            insurance_policy = (
                PatientMapper._insurance_policy_to_domain(
                    model.insurance_policy
                )
            )

        emergency_contacts = [
            PatientMapper._emergency_contact_to_domain(contact)
            for contact in model.emergency_contacts
        ]

        patient = Patient(
            id=model.id,
            medical_record_number=MedicalRecordNumber(
                model.medical_record_number
            ),
            name=PatientName(model.name),
            email=Email(model.email),
            phone_number=PhoneNumber(model.phone_number),
            gender=Gender(model.gender),
            date_of_birth=DateOfBirth(model.date_of_birth),
            address=Address(model.address),
            insurance_policy=insurance_policy,
            emergency_contacts=emergency_contacts,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

        return patient

    # =========================================================
    # DOMAIN → MODEL
    # =========================================================

    @staticmethod
    def to_model(patient: Patient) -> PatientModel:
        """
        Convert a Patient aggregate into SQLAlchemy persistence
        models.

        The returned model graph contains the complete aggregate.
        """

        model = PatientModel(
            id=patient.id,
            medical_record_number=(
                patient.medical_record_number.value
            ),
            name=patient.name.value,
            email=patient.email.value,
            phone_number=patient.phone_number.value,
            gender=patient.gender.value,
            date_of_birth=patient.date_of_birth.value,
            address=patient.address.value,
            active=patient.active,
            created_at=patient.created_at,
            updated_at=patient.updated_at,
        )

        if patient.insurance_policy is not None:
            model.insurance_policy = (
                PatientMapper._insurance_policy_to_model(
                    patient.insurance_policy,
                    patient.id,
                )
            )

        model.emergency_contacts = [
            PatientMapper._emergency_contact_to_model(
                contact,
                patient.id,
            )
            for contact in patient.emergency_contacts
        ]

        return model

    # =========================================================
    # INSURANCE POLICY
    # =========================================================

    @staticmethod
    def _insurance_policy_to_domain(
        model: InsurancePolicyModel,
    ) -> InsurancePolicy:
        return InsurancePolicy(
            id=model.id,
            insurance_number=__import__(
                "patient.domain.value_objects.insurance_number",
                fromlist=["InsuranceNumber"],
            ).InsuranceNumber(
                model.insurance_number
            ),
            provider=model.provider,
            policy_type=model.policy_type,
            effective_date=model.effective_date,
            expiry_date=model.expiry_date,
            status=InsurancePolicyStatus(model.status),
        )

    @staticmethod
    def _insurance_policy_to_model(
        policy: InsurancePolicy,
        patient_id,
    ) -> InsurancePolicyModel:
        return InsurancePolicyModel(
            patient_id=patient_id,
            id=policy.id,
            insurance_number=policy.insurance_number.value,
            provider=policy.provider,
            policy_type=policy.policy_type,
            effective_date=policy.effective_date,
            expiry_date=policy.expiry_date,
            status=policy.status.value,
        )

    # =========================================================
    # EMERGENCY CONTACT
    # =========================================================

    @staticmethod
    def _emergency_contact_to_domain(
        model: EmergencyContactModel,
    ) -> EmergencyContact:
        return EmergencyContact(
            id=model.id,
            name=PatientName(model.name),
            phone_number=PhoneNumber(model.phone_number),
            relationship=model.relationship,
            email=(
                Email(model.email)
                if model.email is not None
                else None
            ),
        )

    @staticmethod
    def _emergency_contact_to_model(
        contact: EmergencyContact,
        patient_id,
    ) -> EmergencyContactModel:
        return EmergencyContactModel(
            id=contact.id,
            patient_id=patient_id,
            name=contact.name.value,
            phone_number=contact.phone_number.value,
            relationship=contact.relationship,
            email=(
                contact.email.value
                if contact.email is not None
                else None
            ),
        )
