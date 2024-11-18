# attendance/views.py
from rest_framework import viewsets
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging

logger = logging.getLogger(__name__)

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f"Attendance marked for student {serializer.data['student']} in course {serializer.data['course']} on {serializer.data['date']}.")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        logger.info(f"Attendance updated for student {serializer.data['student']} in course {serializer.data['course']} on {serializer.data['date']}.")

