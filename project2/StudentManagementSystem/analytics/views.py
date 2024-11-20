from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from rest_framework.permissions import IsAdminUser  
from .models import APIRequestLog
from .serializers import ActiveUserSerializer

class ActiveUsersView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request, *args, **kwargs):
        last_month = timezone.now() - timedelta(days=30)
        active_users = (
            APIRequestLog.objects
            .filter(timestamp__gte=last_month)
            .values('user__username')
            .annotate(request_count=Count('id'))
            .order_by('-request_count')
        )

        serializer = ActiveUserSerializer(active_users, many=True)
        return Response(serializer.data)
