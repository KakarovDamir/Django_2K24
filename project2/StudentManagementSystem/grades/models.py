from django.db import models
from django.conf import settings


class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
    date = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Grade {self.grade} for {self.student.user.username} in {self.course.name}"

