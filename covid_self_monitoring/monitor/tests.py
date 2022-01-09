from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from .factories import UserFactory, SymptomFactory, MeasurementFactory
from .models import Measurement


class TestCreateMeasurement(TestCase):
    def setUp(self):
        self.user_1 = UserFactory()
        self.user_2 = UserFactory()
        self.symptoms = [SymptomFactory() for _ in range(0, 3)]

    def test_create_single_user(self):
        for _ in range(0, 10):
            MeasurementFactory(user=self.user_1, symptoms=self.symptoms)
        self.assertEqual(10, Measurement.objects.count())

    def test_create_multiple_user(self):
        for _ in range(0, 10):
            MeasurementFactory(user=self.user_1, symptoms=self.symptoms)
        for _ in range(0, 5):
            MeasurementFactory(user=self.user_2)
        self.assertEqual(15, Measurement.objects.count())
        self.assertEqual(10, Measurement.objects.filter(user=self.user_1).count())
        self.assertEqual(5, Measurement.objects.filter(user=self.user_2).count())


class TestCreateMeasurementAPI(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.symptoms = [SymptomFactory() for _ in range(0, 3)]
        self.data = {
            'created': timezone.now(),
            'temperature': 36.8,
            'o2sat': 97,
            'systolic': 124,
            'diastolic': 90,
            'symptoms': [model_to_dict(s) for s in self.symptoms]
        }

    def test_create_measurement_api(self):
        response = self.client.post(reverse('measurement-list'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Measurement.objects.filter(user=self.user).count(), 1)
