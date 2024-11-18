from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
import logging
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status


class StudentPagination(PageNumberPagination):
    page_size = 10

logger = logging.getLogger(__name__)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StudentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username', 'dob']

    def list(self, request, *args, **kwargs):
        # Define cache key considering filters and pagination
        cache_key = f"students_list_{request.GET.urlencode()}"
        
        logger.debug(f"Cache Key for students: {cache_key}")

        cached_students = cache.get(cache_key)
        if cached_students:
            logger.debug("Serving from cache")
            return Response(cached_students, status=status.HTTP_200_OK)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        
        logger.debug("Stored to cache")
        
        return response

    def perform_create(self, serializer):
        super().perform_create(serializer)
        # Invalidate related cache on create
        cache.delete_pattern("students_list_*")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Invalidate related cache on update
        cache.delete_pattern("students_list_*")

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        # Invalidate related cache on delete
        cache.delete_pattern("students_list_*")
