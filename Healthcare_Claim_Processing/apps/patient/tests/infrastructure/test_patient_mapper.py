from datetime import date

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

from patient.infrastructure.persistence.mappers.patient_mapper import (
    PatientMapper,
)


def make_patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber(
            "MRN-MAPPER-001"
        ),
        name=PatientName(
            first_name="John",
            last_name="Doe",
        ),
        email=Email("john@example.com"),
        phone_number=PhoneNumber(
            "+2348012345678"
        ),
        gender=Gender.MALE,
        date_of_birth=DateOfBirth(
            date(1990, 1, 1)
        ),
        address=Address(
            street="12 Allen Avenue",
            city="Ikeja",
            state="Lagos",
            postal_code="100001",
            country="NG",
        ),
    )


def test_patient_maps_to_model() -> None:
    patient = make_patient()

    model = PatientMapper.to_model(patient)

    assert model.id == patient.id
    assert (
        model.medical_record_number
        == patient.medical_record_number.value
    )
    assert model.first_name == patient.name.first_name
    assert model.last_name == patient.name.last_name
    assert model.email == patient.email.value
    assert model.phone_number == patient.phone_number.value
    assert model.gender == patient.gender.value
    assert model.date_of_birth == patient.date_of_birth.value
    assert model.street == patient.address.street
    assert model.city == patient.address.city
    assert model.state == patient.address.state
    assert model.postal_code == patient.address.postal_code
    assert model.country == patient.address.country
    assert model.active == patient.active


def test_patient_model_maps_back_to_domain() -> None:
    patient = make_patient()

    model = PatientMapper.to_model(patient)

    restored = PatientMapper.to_domain(model)

    assert restored.id == patient.id

    assert (
        restored.medical_record_number.value
        == patient.medical_record_number.value
    )

    assert (
        restored.name.first_name
        == patient.name.first_name
    )

    assert (
        restored.name.last_name
        == patient.name.last_name
    )

    assert restored.email.value == patient.email.value

    assert (
        restored.phone_number.value
        == patient.phone_number.value
    )

    assert restored.gender == patient.gender

    assert (
        restored.date_of_birth.value
        == patient.date_of_birth.value
    )

    assert restored.address == patient.address

    assert restored.active == patient.active


def test_patient_mapper_round_trip_does_not_create_domain_events() -> None:
    patient = make_patient()

    model = PatientMapper.to_model(patient)

    restored = PatientMapper.to_domain(model)

    assert restored.domain_events == ()