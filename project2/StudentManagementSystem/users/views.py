from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .models import CustomUser
from .serializers import UserSerializer

class AssignRoleView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        user = CustomUser.objects.get(pk=pk)
        role = request.data.get('role')
        if role in dict(CustomUser.ROLE_CHOICES).keys():
            user.role = role
            user.save()
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid role.'}, status=400)

