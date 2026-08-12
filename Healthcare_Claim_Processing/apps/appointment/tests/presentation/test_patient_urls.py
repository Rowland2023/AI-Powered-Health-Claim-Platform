from uuid import uuid4

from django.urls import resolve

from patient.presentation.http.urls import (
    register_patient,
    update_patient_contact_information,
    urlpatterns,
)


def test_register_patient_url_resolves_to_register_view():
    match = resolve(
        "/patients/",
        urlconf=urlpatterns,
    )

    assert match.func is register_patient
    assert match.url_name == "register-patient"


def test_update_patient_contact_information_url_resolves_to_update_view():
    patient_id = uuid4()

    match = resolve(
        f"/patients/{patient_id}/contact-information/",
        urlconf=urlpatterns,
    )

    assert match.func is update_patient_contact_information
    assert match.url_name == "update-patient-contact-information"
    assert match.kwargs["patient_id"] == patient_id