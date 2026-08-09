
from datetime import date

import pytest

from patient.domain.value_objects.address import Address
from patient.domain.value_objects.date_of_birth import DateOfBirth
from patient.domain.value_objects.email import Email
from patient.domain.value_objects.gender import Gender
from patient.domain.value_objects.medical_record_number import (
    MedicalRecordNumber,
)
from patient.domain.value_objects.patient_name import PatientName
from patient.domain.value_objects.phone_number import PhoneNumber


def test_medical_record_number_stores_value():
    value = MedicalRecordNumber("MRN-001")

    assert value.value == "MRN-001"


def test_patient_name_stores_value():
    value = PatientName("John", "Doe")

    assert value.first_name == "John"
    assert value.last_name == "Doe"
    assert value.full_name == "John Doe"


def test_email_stores_value():
    value = Email("john@example.com")

    assert value.value == "john@example.com"


def test_phone_number_stores_value():
    value = PhoneNumber("+2348012345678")

    assert value.value == "+2348012345678"


def test_gender_stores_value():
    value = Gender.from_value("male")

    assert value == Gender.MALE
    assert value.value == "MALE"


def test_address_stores_value():
    value = Address(
        street="12 Allen Avenue",
        city="Ikeja",
        state="Lagos",
        postal_code="100001",
    )

    assert value.street == "12 Allen Avenue"
    assert value.city == "Ikeja"
    assert value.state == "Lagos"
    assert value.postal_code == "100001"
    assert value.country == "NG"


def test_date_of_birth_stores_date():
    value = DateOfBirth(date(1990, 1, 1))

    assert value.value == date(1990, 1, 1)


@pytest.mark.parametrize(
    "factory",
    [
        lambda: MedicalRecordNumber(""),
        lambda: PatientName("", "Doe"),
        lambda: PatientName("John", ""),
        lambda: Email(""),
        lambda: PhoneNumber(""),
        lambda: Address(
            street="",
            city="Lagos",
            state="Lagos",
            postal_code="100001",
        ),
        lambda: Address(
            street="12 Allen Avenue",
            city="",
            state="Lagos",
            postal_code="100001",
        ),
        lambda: Address(
            street="12 Allen Avenue",
            city="Ikeja",
            state="",
            postal_code="100001",
        ),
        lambda: Address(
            street="12 Allen Avenue",
            city="Ikeja",
            state="Lagos",
            postal_code="",
        ),
    ],
)
def test_value_objects_reject_invalid_values(factory):
    with pytest.raises((ValueError, TypeError)):
        factory()
