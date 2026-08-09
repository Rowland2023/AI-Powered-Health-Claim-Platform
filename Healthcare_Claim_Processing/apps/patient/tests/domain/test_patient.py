
# patient/tests/domain/test_patient.py

from datetime import date

import pytest

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


def make_patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber("MRN-001"),
        name=PatientName("John", "Doe"),
        email=Email("john@example.com"),
        phone_number=PhoneNumber("+2348012345678"),
        gender=Gender.from_value("male"),
        date_of_birth=DateOfBirth(date(1990, 1, 1)),
        address=Address(
            street="12 Allen Avenue",
            city="Ikeja",
            state="Lagos",
            postal_code="100001",
        ),
    )


def test_patient_registration_creates_active_patient():
    patient = make_patient()

    assert patient.id is not None
    assert patient.active is True
    assert patient.medical_record_number.value == "MRN-001"


def test_patient_registration_creates_registered_event():
    patient = make_patient()

    events = patient.domain_events

    assert len(events) == 1
    assert events[0].event_name == "PatientRegistered"
    assert events[0].patient_id == patient.id


def test_patient_can_update_contact_information():
    patient = make_patient()

    patient.update_contact_information(
        email=Email("new@example.com"),
        phone_number=PhoneNumber("+2348098765432"),
        address=Address(
            street="1 Independence Avenue",
            city="Abuja",
            state="FCT",
            postal_code="900001",
        ),
    )

    assert patient.email.value == "new@example.com"
    assert patient.phone_number.value == "+2348098765432"
    assert patient.address.city == "Abuja"


def test_patient_update_creates_patient_updated_event():
    patient = make_patient()

    patient.clear_domain_events()

    patient.update_contact_information(
        email=Email("new@example.com"),
        phone_number=PhoneNumber("+2348098765432"),
        address=Address(
            street="1 Independence Avenue",
            city="Abuja",
            state="FCT",
            postal_code="900001",
        ),
    )

    events = patient.domain_events

    assert len(events) == 1
    assert events[0].event_name == "PatientUpdated"
    assert events[0].patient_id == patient.id


def test_patient_can_be_deactivated():
    patient = make_patient()

    patient.clear_domain_events()

    patient.deactivate()

    assert patient.active is False

    events = patient.domain_events

    assert len(events) == 1
    assert events[0].event_name == "PatientDeactivated"


def test_patient_deactivation_is_idempotent():
    patient = make_patient()

    patient.clear_domain_events()

    patient.deactivate()
    patient.clear_domain_events()

    patient.deactivate()

    assert patient.active is False
    assert patient.domain_events == ()


def test_patient_can_be_reactivated():
    patient = make_patient()

    patient.deactivate()
    patient.clear_domain_events()

    patient.activate()

    assert patient.active is True

    events = patient.domain_events

    assert len(events) == 1
    assert events[0].event_name == "PatientUpdated"


def test_patient_activation_is_idempotent():
    patient = make_patient()

    patient.clear_domain_events()

    patient.activate()

    assert patient.active is True
    assert patient.domain_events == ()

# patient/tests/domain/test_patient_events.py

from datetime import date

from patient.domain.entities.patient import Patient
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


def make_patient() -> Patient:
    return Patient.register(
        medical_record_number=MedicalRecordNumber("MRN-001"),
        name=PatientName("John", "Doe"),
        email=Email("john@example.com"),
        phone_number=PhoneNumber("+2348012345678"),
        gender=Gender.from_value("male"),
        date_of_birth=DateOfBirth(date(1990, 1, 1)),
        address=Address(
            street="12 Allen Avenue",
            city="Ikeja",
            state="Lagos",
            postal_code="100001",
        ),
    )


def test_patient_registered_event_contains_patient_id():
    patient = make_patient()

    event = patient.domain_events[0]

    assert isinstance(event, PatientRegistered)
    assert event.patient_id == patient.id
    assert event.aggregate_id == patient.id


def test_patient_registered_event_has_event_metadata():
    patient = make_patient()

    event = patient.domain_events[0]

    assert event.event_id is not None
    assert event.event_name == "PatientRegistered"
    assert event.event_version == 1
    assert event.occurred_at is not None


def test_patient_updated_event_contains_patient_id():
    patient = make_patient()

    patient.clear_domain_events()

    patient.update_contact_information(
        email=Email("new@example.com"),
        phone_number=PhoneNumber("+2348098765432"),
        address=Address(
            street="1 Independence Avenue",
            city="Abuja",
            state="FCT",
            postal_code="900001",
        ),
    )

    event = patient.domain_events[0]

    assert isinstance(event, PatientUpdated)
    assert event.patient_id == patient.id
    assert event.aggregate_id == patient.id


def test_patient_deactivated_event_contains_patient_id():
    patient = make_patient()

    patient.clear_domain_events()

    patient.deactivate()

    event = patient.domain_events[0]

    assert isinstance(event, PatientDeactivated)
    assert event.patient_id == patient.id
    assert event.aggregate_id == patient.id
