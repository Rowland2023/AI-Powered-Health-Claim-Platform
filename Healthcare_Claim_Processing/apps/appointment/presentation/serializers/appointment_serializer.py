from rest_framework import serializers

from appointment.domain.value_objects.appointment_type import (
    AppointmentType,
)


class ScheduleAppointmentSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField()
    provider_id = serializers.UUIDField()
    appointment_type = serializers.ChoiceField(
        choices=[appointment_type.value for appointment_type in AppointmentType]
    )
    scheduled_at = serializers.DateTimeField()
    reason = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True,
    )