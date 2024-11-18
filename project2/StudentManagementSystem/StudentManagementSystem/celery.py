from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StudentManagementSystem.settings')
app = Celery('StudentManagementSystem')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()