from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    TYPE_CHOICES = (
        ('ATTENDANCE_REMINDER', 'Attendance Reminder'),
        ('GRADE_UPDATE', 'Grade Update'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} for {self.user.username} - {'Read' if self.is_read else 'Unread'}"

    class Meta:
        ordering = ['-created_at']

