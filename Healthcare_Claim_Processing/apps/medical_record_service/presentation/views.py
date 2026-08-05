from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CreateMedicalRecordSerializer


class MedicalRecordListView(APIView):

    def post(self, request):

        serializer = CreateMedicalRecordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        #
        # call application layer
        #

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED
        )