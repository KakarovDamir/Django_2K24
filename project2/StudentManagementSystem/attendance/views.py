from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger(__name__)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]

    @swagger_auto_schema(
        operation_description="Retrieve a list of attendance records.",
        responses={200: AttendanceSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new attendance record.",
        request_body=AttendanceSerializer,
        responses={201: AttendanceSerializer, 400: "Bad request"}
    )
    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f"Attendance marked for student {serializer.data['student']} in course {serializer.data['course']} on {serializer.data['date']}.")

    @swagger_auto_schema(
        operation_description="Retrieve an attendance record by ID.",
        responses={200: AttendanceSerializer, 404: "Not found"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an attendance record.",
        request_body=AttendanceSerializer,
        responses={200: AttendanceSerializer, 400: "Bad request", 404: "Not found"}
    )
    def perform_update(self, serializer):
        super().perform_update(serializer)
        logger.info(f"Attendance updated for student {serializer.data['student']} in course {serializer.data['course']} on {serializer.data['date']}.")

    @swagger_auto_schema(
        operation_description="Delete an attendance record.",
        responses={204: "No content", 404: "Not found"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)