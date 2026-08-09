from __future__ import annotations

from patient.composition import create_patient_dependencies
from patient.presentation.http.views import (
    PatientContactInformationView,
    PatientRegistrationView,
)


def configure_patient_views():
    """
    Compose the Patient bounded context for Django.

    Dependencies are created once and injected into the
    HTTP views.
    """

    dependencies = create_patient_dependencies()

    controller = dependencies["patient_controller"]

    class ConfiguredPatientRegistrationView(
        PatientRegistrationView
    ):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._controller = controller

    class ConfiguredPatientContactInformationView(
        PatientContactInformationView
    ):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self._controller = controller

    return (
        ConfiguredPatientRegistrationView,
        ConfiguredPatientContactInformationView,
    )