from django.core.management.base import BaseCommand
from analytics.models import APIRequestLog
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count  

class Command(BaseCommand):
    help = 'Report most active users over the last month'

    def handle(self, *args, **kwargs):
        last_month = timezone.now() - timedelta(days=30)
        active_users = (
            APIRequestLog.objects
            .filter(timestamp__gte=last_month)
            .values('user__username')
            .annotate(request_count=Count('id'))
            .order_by('-request_count')
        )
        for user in active_users:
            self.stdout.write(f"User: {user['user__username']}, Requests: {user['request_count']}")