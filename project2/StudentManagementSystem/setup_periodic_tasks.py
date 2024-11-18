import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagementSystem.settings')
django.setup()

from django_celery_beat.models import CrontabSchedule, PeriodicTask
