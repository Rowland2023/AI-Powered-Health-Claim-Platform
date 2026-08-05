from rest_framework import serializers


class CreateMedicalRecordSerializer(serializers.Serializer):

    patient_id = serializers.UUIDField()

    diagnosis = serializers.CharField()

    allergies = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )

    clinical_notes = serializers.CharField()

    attending_physician = serializers.UUIDField()