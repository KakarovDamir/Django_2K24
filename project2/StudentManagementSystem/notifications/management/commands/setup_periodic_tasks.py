from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule

class Command(BaseCommand):
    help = 'Set up periodic tasks for Celery Beat'

    def handle(self, *args, **kwargs):
        daily_schedule, _ = CrontabSchedule.objects.get_or_create(hour=7, minute=0)
        PeriodicTask.objects.get_or_create(
            crontab=daily_schedule,
            name='Send Daily Attendance Reminder',
            task='notifications.tasks.send_daily_attendance_reminder',
        )

        weekly_schedule, _ = CrontabSchedule.objects.get_or_create(day_of_week='mon', hour=8, minute=0)
        PeriodicTask.objects.get_or_create(
            crontab=weekly_schedule,
            name='Send Weekly Performance Summary',
            task='notifications.tasks.send_weekly_performance_summary',
        )

        self.stdout.write(self.style.SUCCESS('Successfully set up periodic tasks'))

