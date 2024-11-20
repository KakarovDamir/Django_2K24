from rest_framework.test import APITestCase
from rest_framework import status
from ..models import Course
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse 

User = get_user_model()

class CourseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teacher', password='12345', role='TEACHER')
        
        self.client.login(username='teacher', password='12345')

        self.course_data = {'name': 'Mathematics', 'description': 'Basic Math Course', 'instructor': self.user.id}

    def test_create_course(self):
        create_course_url = reverse('course-list')
        response = self.client.post(create_course_url, self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_courses(self):
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_role_based_access_control(self):
        response = self.client.post('/api/courses/', self.course_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
