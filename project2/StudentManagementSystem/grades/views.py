# grades/views.py
from rest_framework import viewsets
from .models import Grade
from .serializers import GradeSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging

logger = logging.getLogger(__name__)

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f"Grade {serializer.data['grade']} added for student {serializer.data['student']} in course {serializer.data['course']}.")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        logger.info(f"Grade updated to {serializer.data['grade']} for student {serializer.data['student']} in course {serializer.data['course']}.")

