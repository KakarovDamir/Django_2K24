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
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from analytics.models import APIRequestLog, CoursePopularity


class CoursePagination(PageNumberPagination):
    page_size = 10

logger = logging.getLogger(__name__)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
    pagination_class = CoursePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'instructor__username']
    
    @swagger_auto_schema(
        operation_description="Retrieve a list of courses with filtering and pagination.",
        responses={200: CourseSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by course name", type=openapi.TYPE_STRING),
            openapi.Parameter('instructor__username', openapi.IN_QUERY, description="Filter by instructor username", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        cache_key = f"courses_list_{request.GET.urlencode()}"
        logger.debug(f"Cache Key for courses: {cache_key}")

        # Log the request for analytics
        if request.user.is_authenticated:
            APIRequestLog.objects.create(user=request.user, path=request.path, method=request.method)

        cached_courses = cache.get(cache_key)
        if cached_courses:
            logger.debug("Serving from cache")
            return Response(cached_courses, status=status.HTTP_200_OK)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=300)
        
        for course_data in response.data:
            try:
                course = Course.objects.get(id=course_data['id'])
                course_popularity, _ = CoursePopularity.objects.get_or_create(course=course)
                course_popularity.increment_views()
            except Course.DoesNotExist:
                pass

        logger.debug("Stored to cache")
        
        return response

    @swagger_auto_schema(
        operation_description="Create a new course.",
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: "Bad request"}
    )
    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.delete_pattern("courses_list_*")
        if self.request.user.is_authenticated:
            APIRequestLog.objects.create(user=self.request.user, path=self.request.path, method='POST')

    @swagger_auto_schema(
        operation_description="Update an existing course.",
        request_body=CourseSerializer,
        responses={200: CourseSerializer, 400: "Bad request", 404: "Not found"}
    )
    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.delete_pattern("courses_list_*")
        if self.request.user.is_authenticated:
            APIRequestLog.objects.create(user=self.request.user, path=self.request.path, method='PUT')

    @swagger_auto_schema(
        operation_description="Delete a course.",
        responses={204: "No content", 404: "Not found"}
    )
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.delete_pattern("courses_list_*")
        if self.request.user.is_authenticated:
            APIRequestLog.objects.create(user=self.request.user, path=self.request.path, method='DELETE')

class EnrollmentViewSet(viewsets.ModelViewSet):
       queryset = Enrollment.objects.all()
       serializer_class = EnrollmentSerializer
       permission_classes = [IsAuthenticated, IsTeacher | IsAdmin]
       
       @swagger_auto_schema(
           operation_description="Create a new enrollment.",
           request_body=EnrollmentSerializer,
           responses={201: EnrollmentSerializer, 400: "Bad request"}
       )
       def perform_create(self, serializer):
           super().perform_create(serializer)
           logger.info(f"Student {serializer.data['student']} enrolled in course {serializer.data['course']}.")
           if self.request.user.is_authenticated:
               APIRequestLog.objects.create(user=self.request.user, path=self.request.path, method='POST')

       @swagger_auto_schema(
           operation_description="Delete an enrollment.",
           responses={204: "No content", 404: "Not found"}
       )
       def perform_destroy(self, instance):
           super().perform_destroy(instance)
           logger.info(f"Student {instance.student} unenrolled from course {instance.course}.")
           if self.request.user.is_authenticated:
               APIRequestLog.objects.create(user=self.request.user, path=self.request.path, method='DELETE')