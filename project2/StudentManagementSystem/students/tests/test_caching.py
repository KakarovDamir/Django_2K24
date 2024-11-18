# students/tests/test_caching.py

import logging
from django.core.cache import cache
from rest_framework.test import APITestCase

logger = logging.getLogger(__name__)

class CachingTest(APITestCase):
    def test_caching(self):
        response1 = self.client.get('/api/students/')
        self.assertIsNone(cache.get('students_list_'))

        # Cache the first response
        cache.set('students_list_', response1.data, timeout=300)

        # Check if data is cached
        cached_response = cache.get('students_list_')
        self.assertEqual(response1.data, cached_response)

        # Perform any update that should invalidate cache
        # Ensure cache is now invalidated and a new request establishes new cached data
