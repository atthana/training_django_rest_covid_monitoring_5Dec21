from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Measurement

User = get_user_model()


class MeasurementSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(default=timezone.now())

    class Meta:
        model = Measurement
        fields = ['id', 'created', 'temperature', 'o2sat', 'systolic', 'diastolic', 'user']


