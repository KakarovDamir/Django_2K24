from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Course, Enrollment
from .serializers import CourseSerializer, EnrollmentSerializer
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTeacher, IsAdmin
import logging
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

class CoursePagination(PageNumberPagination):
    page_size = 10

# Initialize a logger for debugging
logger = logging.getLogger(__name__)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'instructor__username']

    def list(self, request, *args, **kwargs):
        # Define cache key considering filters
        cache_key = f"courses_list_{request.GET.urlencode()}"
        
        logger.debug(f"Cache Key for courses: {cache_key}")
        
        # Attempt to retrieve the cached data
        cached_courses = cache.get(cache_key)
        
        if cached_courses:
            logger.debug("Serving from cache")
            return Response(cached_courses, status=status.HTTP_200_OK)

        # Proceed with default list retrieval if no cached data
        response = super().list(request, *args, **kwargs)
        # Cache the response data
        cache.set(cache_key, response.data, timeout=300)
        
        logger.debug("Stored to cache")
        
        return response

    def perform_create(self, serializer):
        super().perform_create(serializer)
        # Invalidate related cache on create
        cache.delete_pattern("courses_list_*")

    def perform_update(self, serializer):
        super().perform_update(serializer)
        # Invalidate related cache on update
        cache.delete_pattern("courses_list_*")

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        # Invalidate related cache on delete
        cache.delete_pattern("courses_list_*")

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
    
    def perform_create(self, serializer):
        super().perform_create(serializer)
        logger.info(f"Student {serializer.data['student']} enrolled in course {serializer.data['course']}.")

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        logger.info(f"Student {instance.student} unenrolled from course {instance.course}.")
