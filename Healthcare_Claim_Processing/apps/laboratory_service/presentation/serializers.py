# apps/laboratory/presentation/serializers.py

from rest_framework import serializers

class ValidateLabResultInputSerializer(serializers.Serializer):
    pathologist_id = serializers.UUIDField(
        required=True,
        help_text="UUID of the certifying pathologist validating the results."
    )


class LabOrderPathParameterSerializer(serializers.Serializer):
    order_id = serializers.UUIDField(
        required=True,
        help_text="UUID of the laboratory order."
    )