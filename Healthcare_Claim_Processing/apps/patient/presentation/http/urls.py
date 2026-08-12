from __future__ import annotations

from django.urls import path

from patient.composition import create_patient_dependencies
from patient.presentation.http.views import create_patient_views


dependencies = create_patient_dependencies()

(
    register_patient,
    update_patient_contact_information,
) = create_patient_views(
    dependencies["patient_controller"]
)


app_name = "patient"


urlpatterns = [
    path(
        "patients/",
        register_patient,
        name="register-patient",
    ),
    path(
        "patients/<uuid:patient_id>/contact-information/",
        update_patient_contact_information,
        name="update-patient-contact-information",
    ),
]
