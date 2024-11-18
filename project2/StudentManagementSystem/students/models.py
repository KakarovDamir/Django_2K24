# students/models.py
from django.db import models
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField("Date of Birth")
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

