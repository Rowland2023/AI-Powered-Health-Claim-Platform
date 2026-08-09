
from __future__ import annotations

from dataclasses import dataclass

from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber


@dataclass(frozen=True)
class RegisterPatientCommand:
    """
    Application command requesting registration of a new patient.

    The command carries data into the application layer.
    It does not perform domain behavior itself.
    """

    medical_record_number: MedicalRecordNumber
    name: PatientName
    email: Email
    phone_number: PhoneNumber
    gender: Gender
    date_of_birth: DateOfBirth
    address: Address
