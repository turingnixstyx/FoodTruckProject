from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from .models import TruckModel
from .views import TruckModelCreateView
from .utils import calculate_distance
import json


class TruckModelTestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_if_relative_distance(self) -> None:
        pass

    def test_model_name(self) -> None:
        pass

    def check_db_index(self) -> None:
        pass


class TruckModelViewTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_details(self) -> None:
        request = self.factory.post("location/1")
        request.user = AnonymousUser()
        request.body = json.dumps(
            {'x': "50", 'y': "-114.97889783", 'radius': "190.9898"}).encode('utf-8')

        response = TruckModelCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)
