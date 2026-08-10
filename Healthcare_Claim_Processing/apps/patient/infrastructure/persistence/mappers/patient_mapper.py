
from __future__ import annotations

from patient.domain.entities.emergency_contact import EmergencyContact
from patient.domain.entities.insurance_policy import InsurancePolicy
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
from patient.infrastructure.persistence.models.patient_model import PatientModel


class PatientMapper:
    """
    Maps between the Patient domain aggregate and its
    SQLAlchemy persistence representation.

    Infrastructure concern only.

    Domain objects never know that this mapper exists.
    """

    # ---------------------------------------------------------
    # Patient -> SQLAlchemy model
    # ---------------------------------------------------------

    @staticmethod
    def to_model(patient: Patient) -> PatientModel:
        """
        Convert a Patient aggregate into a SQLAlchemy model.
        """

        insurance_policy = None

        if patient.insurance_policy is not None:
            insurance_policy = InsurancePolicyModel(
                provider=patient.insurance_policy.provider,
                policy_number=patient.insurance_policy.policy_number,
            )

        emergency_contacts = [
            EmergencyContactModel(
                id=contact.id,
                name=contact.name,
                phone_number=contact.phone_number,
                contact_relationship=contact.relationship,
                email=contact.email,
            )
            for contact in patient.emergency_contacts
        ]

        return PatientModel(
            id=patient.id,
            medical_record_number=patient.medical_record_number.value,
            first_name=patient.name.first_name,
            last_name=patient.name.last_name,
            email=patient.email.value,
            phone_number=patient.phone_number.value,
            gender=patient.gender.value,
            date_of_birth=patient.date_of_birth.value,
            street=patient.address.street,
            city=patient.address.city,
            state=patient.address.state,
            postal_code=patient.address.postal_code,
            country=patient.address.country,
            active=patient.active,
            created_at=patient.created_at,
            updated_at=patient.updated_at,
            insurance_policy=insurance_policy,
            emergency_contacts=emergency_contacts,
        )

    # ---------------------------------------------------------
    # SQLAlchemy model -> Patient
    # ---------------------------------------------------------

    @staticmethod
    def to_domain(model: PatientModel) -> Patient:
        """
        Convert a SQLAlchemy model into a Patient aggregate.

        This reconstructs the Patient aggregate and all of its
        owned entities/value objects.
        """

        insurance_policy = None

        if model.insurance_policy is not None:
            insurance_policy = InsurancePolicy(
                provider=model.insurance_policy.provider,
                policy_number=model.insurance_policy.policy_number,
            )

        emergency_contacts = [
            EmergencyContact(
                id=contact.id,
                name=contact.name,
                phone_number=contact.phone_number,
                relationship=contact.contact_relationship,
                email=contact.email,
            )
            for contact in model.emergency_contacts
        ]

        return Patient(
            id=model.id,
            medical_record_number=MedicalRecordNumber(
                model.medical_record_number
            ),
            name=PatientName(
                first_name=model.first_name,
                last_name=model.last_name,
            ),
            email=Email(model.email),
            phone_number=PhoneNumber(model.phone_number),
            gender=Gender.from_value(model.gender),
            date_of_birth=DateOfBirth.from_date(
                model.date_of_birth
            ),
            address=Address(
                street=model.street,
                city=model.city,
                state=model.state,
                postal_code=model.postal_code,
                country=model.country,
            ),
            insurance_policy=insurance_policy,
            emergency_contacts=emergency_contacts,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
