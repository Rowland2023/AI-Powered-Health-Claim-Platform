from rest_framework import serializers


class CreateLabOrderInputSerializer(serializers.Serializer):
    patient_id = serializers.UUIDField()
    encounter_id = serializers.UUIDField()
    ordering_physician_id = serializers.UUIDField()


class CollectSpecimenInputSerializer(serializers.Serializer):
    specimen_type = serializers.CharField(max_length=50)
    barcode = serializers.CharField(min_length=5, max_length=100)


class ValidateLabResultInputSerializer(serializers.Serializer):
    """
    The pathologist is resolved from the authenticated account.
    Never accept pathologist_id from the request body.
    """

    pass


class LabOrderPathParameterSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
