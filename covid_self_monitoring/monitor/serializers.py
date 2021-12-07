from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Measurement, Symptom

User = get_user_model()


class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(default=timezone.now())
    symptoms = SymptomSerializer(many=True)
    # symptoms ตรงนี้เราจะ serialize มันออกไปอย่างไร ก็เอามาจาก SymptomSerializer ไง
    # เป็นการ serialize ตัว many to many ออกมา แล้วได้ทั้ง key และ value ออกมา

    class Meta:
        model = Measurement
        fields = '__all__'


