from unittest.mock import patch
from django.test import TestCase
from ..tasks import send_daily_attendance_reminder

class AttendanceReminderTest(TestCase):
    @patch('notifications.tasks.send_mail')
    def test_send_daily_attendance_reminder(self, mock_send_mail):
        send_daily_attendance_reminder()
        self.assertTrue(mock_send_mail.called)

