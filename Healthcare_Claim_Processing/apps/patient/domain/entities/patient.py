
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from shared.domain.aggregate_root import AggregateRoot

from patient.domain.entities.emergency_contact import EmergencyContact
from patient.domain.entities.insurance_policy import InsurancePolicy

from patient.domain.events.patient_deactivated import PatientDeactivated
from patient.domain.events.patient_registered import PatientRegistered
from patient.domain.events.patient_updated import PatientUpdated

from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber


@dataclass
class Patient(AggregateRoot):
    """
    Aggregate Root representing a patient.

    Patient owns the lifecycle and consistency rules for
    patient information.
    """

    id: UUID

    medical_record_number: MedicalRecordNumber

    name: PatientName

    email: Email

    phone_number: PhoneNumber

    gender: Gender

    date_of_birth: DateOfBirth

    address: Address

    insurance_policy: InsurancePolicy | None = None

    emergency_contacts: list[EmergencyContact] = field(
        default_factory=list
    )

    active: bool = True

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        """
        Initialize the AggregateRoot state.

        Because Patient is a dataclass, its generated __init__()
        does not automatically call AggregateRoot.__init__().
        """

        AggregateRoot.__init__(self)

    # =========================================================
    # FACTORY
    # =========================================================

    @classmethod
    def register(
        cls,
        *,
        medical_record_number: MedicalRecordNumber,
        name: PatientName,
        email: Email,
        phone_number: PhoneNumber,
        gender: Gender,
        date_of_birth: DateOfBirth,
        address: Address,
        insurance_policy: InsurancePolicy | None = None,
    ) -> "Patient":
        """
        Create and register a new Patient aggregate.

        PatientRegistered is raised as a consequence of the
        successful creation of the aggregate.
        """

        patient = cls(
            id=uuid4(),
            medical_record_number=medical_record_number,
            name=name,
            email=email,
            phone_number=phone_number,
            gender=gender,
            date_of_birth=date_of_birth,
            address=address,
            insurance_policy=insurance_policy,
        )

        patient.add_domain_event(
            PatientRegistered(
                aggregate_id=patient.id,
                patient_id=patient.id,
            )
        )

        return patient

    # =========================================================
    # CONTACT INFORMATION
    # =========================================================

    def update_contact_information(
        self,
        *,
        email: Email,
        phone_number: PhoneNumber,
        address: Address,
    ) -> None:
        """
        Update patient contact information.

        The aggregate records the resulting domain event.
        """

        self.email = email
        self.phone_number = phone_number
        self.address = address

        self._touch()

        self.add_domain_event(
            PatientUpdated(
                aggregate_id=self.id,
                patient_id=self.id,
            )
        )

    # =========================================================
    # INSURANCE
    # =========================================================

    def update_insurance(
        self,
        insurance_policy: InsurancePolicy,
    ) -> None:
        """
        Replace or update the patient's insurance policy.
        """

        self.insurance_policy = insurance_policy

        self._touch()

        self.add_domain_event(
            PatientUpdated(
                aggregate_id=self.id,
                patient_id=self.id,
            )
        )

    # =========================================================
    # EMERGENCY CONTACTS
    # =========================================================

    def add_emergency_contact(
        self,
        contact: EmergencyContact,
    ) -> None:
        """
        Add an emergency contact to the patient.
        """

        self.emergency_contacts.append(contact)

        self._touch()

        self.add_domain_event(
            PatientUpdated(
                aggregate_id=self.id,
                patient_id=self.id,
            )
        )

    # =========================================================
    # DEACTIVATION
    # =========================================================

    def deactivate(self) -> None:
        """
        Deactivate the patient.

        Deactivation is idempotent. Calling deactivate()
        on an already inactive patient produces no new event.
        """

        if not self.active:
            return

        self.active = False

        self._touch()

        self.add_domain_event(
            PatientDeactivated(
                aggregate_id=self.id,
                patient_id=self.id,
            )
        )

    # =========================================================
    # ACTIVATION
    # =========================================================

    def activate(self) -> None:
        """
        Reactivate an inactive patient.

        Activation is idempotent. Calling activate()
        on an already active patient produces no new event.
        """

        if self.active:
            return

        self.active = True

        self._touch()

        self.add_domain_event(
            PatientUpdated(
                aggregate_id=self.id,
                patient_id=self.id,
            )
        )

    # =========================================================
    # INTERNAL HELPERS
    # =========================================================

    def _touch(self) -> None:
        """
        Update the aggregate modification timestamp.
        """

        self.updated_at = datetime.now(timezone.utc)
