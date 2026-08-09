
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from patient.domain.value_objects.address import Address
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.phone_number import PhoneNumber


@dataclass(frozen=True)
class UpdatePatientContactCommand:
    """
    Application command requesting an update to
    patient contact information.
    """

    patient_id: UUID
    email: Email
    phone_number: PhoneNumber
    address: Address
