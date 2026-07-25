from django.shortcuts import render

# Create your views here.
# apps/laboratory/presentation/views.py
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.laboratory.application.use_cases.validate_lab_result import ValidateLabResultUseCase
from apps.laboratory.presentation.serializers import ValidateLabResultInputSerializer
from apps.laboratory.domain.exceptions import LabOrderNotFoundException, DomainValidationException

class ValidateLabResultAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def __init__(self, use_case: ValidateLabResultUseCase, **kwargs):
        super().__init__(**kwargs)
        self.use_case = use_case  # Injected from composition root, no fallback

    def post(self, request, order_id: str):
        try:
            parsed_order_id = uuid.UUID(order_id)
        except ValueError:
            return Response({"error": "Invalid UUID"}, status=400)

        serializer = ValidateLabResultInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            # Pass User from request, not from body - pathologist is authenticated user
            result = self.use_case.execute(
                order_id=parsed_order_id,
                pathologist_id=request.user.id, # NEVER trust pathologist_id from client body
                correlation_id=request.headers.get('X-Correlation-ID'),
            )
        except LabOrderNotFoundException:
            return Response({"error": "Order not found"}, status=404)
        except DomainValidationException as e:
            return Response({"error": str(e)}, status=422) # 422 for domain rule violation

        return Response({
            "order_id": str(result.order_id),
            "status": result.status.value,
            "validated_at": result.validated_at.isoformat()
        }, status=200)