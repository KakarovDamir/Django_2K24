from rest_framework.test import APITestCase
from rest_framework import status
from ..models import CustomUser

class RolePermissionsTest(APITestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(username='admin', password='12345', role='ADMIN')
        self.student = CustomUser.objects.create_user(username='student', password='12345', role='STUDENT')

    def test_student_access(self):
        self.client.login(username='student', password='12345')
        response = self.client.post('/api/courses/', {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_access(self):
        self.client.login(username='admin', password='12345')
        response = self.client.post('/api/courses/', {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
