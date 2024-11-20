from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .models import CustomUser
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class AssignRoleView(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="Assign a role to a user by ID",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'role': openapi.Schema(type=openapi.TYPE_STRING, description='Role to assign')
            },
            required=['role']
        ),
        responses={
            200: UserSerializer,
            400: 'Invalid role provided',
            404: 'User not found'
        },
        manual_parameters=[
            openapi.Parameter('pk', openapi.IN_PATH, description="User ID", type=openapi.TYPE_INTEGER)
        ]
    )
    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            role = request.data.get('role')
            if role in dict(CustomUser.ROLE_CHOICES).keys():
                user.role = role
                user.save()
                return Response(UserSerializer(user).data)
            return Response({'error': 'Invalid role.'}, status=400)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=404)
