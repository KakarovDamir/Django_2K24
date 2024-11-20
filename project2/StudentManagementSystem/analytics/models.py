from django.db import models
from django.conf import settings
from courses.models import Course

class APIRequestLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

class CoursePopularity(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def increment_views(self):
        self.views += 1
        self.save()

