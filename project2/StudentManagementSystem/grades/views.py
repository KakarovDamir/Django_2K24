from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger(__name__)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    @swagger_auto_schema(
        operation_description="List all grades, with filtering and pagination support.",
        responses={200: GradeSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new grade.",
        request_body=GradeSerializer,
        responses={201: GradeSerializer, 400: "Bad request"}
    )
    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f"Grade {serializer.data['grade']} added for student {serializer.data['student']} in course {serializer.data['course']}.")

    @swagger_auto_schema(
        operation_description="Retrieve a grade by ID.",
        responses={200: GradeSerializer, 404: "Not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an existing grade.",
        request_body=GradeSerializer,
        responses={200: GradeSerializer, 400: "Bad request", 404: "Not found"}
    )
    def perform_update(self, serializer):
        super().perform_update(serializer)
        logger.info(f"Grade updated to {serializer.data['grade']} for student {serializer.data['student']} in course {serializer.data['course']}.")

    @swagger_auto_schema(
        operation_description="Delete a grade.",
        responses={204: "No content", 404: "Not found"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)