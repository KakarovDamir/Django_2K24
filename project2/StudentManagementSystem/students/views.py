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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

    @swagger_auto_schema(
        operation_description="Retrieve a list of students with filtering and pagination support.",
        responses={200: StudentSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('user__username', openapi.IN_QUERY, description="Filter by username", type=openapi.TYPE_STRING),
            openapi.Parameter('dob', openapi.IN_QUERY, description="Filter by date of birth", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ]
    )
    def list(self, request, *args, **kwargs):
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

    @swagger_auto_schema(
        operation_description="Create a new student.",
        request_body=StudentSerializer,
        responses={201: StudentSerializer, 400: "Bad request"}
    )
    def perform_create(self, serializer):
        super().perform_create(serializer)
        cache.delete_pattern("students_list_*")

    @swagger_auto_schema(
        operation_description="Update a student record.",
        request_body=StudentSerializer,
        responses={200: StudentSerializer, 400: "Bad request", 404: "Not found"}
    )
    def perform_update(self, serializer):
        super().perform_update(serializer)
        cache.delete_pattern("students_list_*")

    @swagger_auto_schema(
        operation_description="Delete a student record.",
        responses={204: "No content", 404: "Not found"}
    )
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.delete_pattern("students_list_*")
