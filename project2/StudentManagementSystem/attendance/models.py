from django.db import models

class Attendance(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('PRESENT', 'Present'), ('ABSENT', 'Absent')])

    def __str__(self):
        return f"{self.student.user.username} was {self.status} on {self.date}"

