from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from enum import Enum
from uuid import UUID

from django.http import Http404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.laboratory_service.application.use_cases.attach_result import (
    AttachLabResultUseCase,
)
from apps.laboratory_service.application.use_cases.collect_specimen import (
    CollectSpecimenUseCase,
)
from apps.laboratory_service.application.use_cases.create_order import (
    CreateLabOrderUseCase,
)
from apps.laboratory_service.application.use_cases.dto import (
    CollectSpecimenInputDTO,
    CreateOrderInputDTO,
    ValidateResultInputDTO,
)
from apps.laboratory_service.application.use_cases.validate_result import (
    ValidateLabResultUseCase,
)
from apps.laboratory_service.domain.exceptions import (
    LaboratoryDomainException,
    OrderNotFoundException,
)
from apps.laboratory_service.infrastructure.orm.models import (
    PathologistIdentityORMModel,
)
from apps.laboratory_service.infrastructure.outbox_writer import (
    write_laboratory_outbox_events,
)
from apps.laboratory_service.infrastructure.repositories.laboratory_repositories import (
    LaboratoryRepository,
)
from apps.laboratory_service.presentation.serializers import (
    CollectSpecimenInputSerializer,
    CreateLabOrderInputSerializer,
    ValidateLabResultInputSerializer,
)


def _json_value(value):
    """Convert DTOs and domain values into JSON-safe response values."""
    if is_dataclass(value):
        return _json_value(asdict(value))
    if isinstance(value, dict):
        return {key: _json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_value(item) for item in value]
    if isinstance(value, (UUID, datetime, date)):
        return value.isoformat() if isinstance(value, (datetime, date)) else str(value)
    if isinstance(value, Enum):
        return value.value
    return value


class LaboratoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_repository(self):
        return LaboratoryRepository(
            outbox_writer=write_laboratory_outbox_events,
        )


class CreateLabOrderAPIView(LaboratoryAPIView):
    def post(self, request):
        serializer = CreateLabOrderInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            dto = CreateOrderInputDTO(**serializer.validated_data)
            result = CreateLabOrderUseCase(self.get_repository()).execute(dto)
        except LaboratoryDomainException as exc:
            return Response(
                exc.to_dict(),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(_json_value(result), status=status.HTTP_201_CREATED)


class CollectSpecimenAPIView(LaboratoryAPIView):
    def post(self, request, order_id):
        serializer = CollectSpecimenInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            dto = CollectSpecimenInputDTO(
                order_id=order_id,
                **serializer.validated_data,
            )
            result = CollectSpecimenUseCase(self.get_repository()).execute(dto)
        except OrderNotFoundException:
            return Response(
                {"error": "Laboratory order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except LaboratoryDomainException as exc:
            return Response(
                exc.to_dict(),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(_json_value(result), status=status.HTTP_200_OK)


class ValidateLabResultAPIView(LaboratoryAPIView):
    def post(self, request, order_id):
        if "pathologist_id" in request.data:
            return Response(
                {"error": "Do not supply pathologist_id in the request body."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ValidateLabResultInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            identity = PathologistIdentityORMModel.objects.get(
                user=request.user,
                is_active=True,
            )
        except PathologistIdentityORMModel.DoesNotExist:
            return Response(
                {"error": "An active pathologist identity is required."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            dto = ValidateResultInputDTO(
                order_id=order_id,
                pathologist_id=identity.pathologist_id,
            )
            result = ValidateLabResultUseCase(
                self.get_repository()
            ).execute(dto)
        except OrderNotFoundException:
            return Response(
                {"error": "Laboratory order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except LaboratoryDomainException as exc:
            return Response(
                exc.to_dict(),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        return Response(_json_value(result), status=status.HTTP_200_OK)
