from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class TruckModelViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create(self):
        url = reverse('truck-list')
        # Example coordinates and radius
        data = {'x': 40.7128, 'y': -74.0060, 'radius': 100}
        response = self.client.post(url, data)

        # Assert response status code
        self.assertEqual(response.status_code, 200)
