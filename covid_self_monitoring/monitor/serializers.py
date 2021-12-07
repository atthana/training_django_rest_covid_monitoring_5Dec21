from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Measurement

User = get_user_model()


class MeasurementSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)  # เราจะทำตาม model field ของเราไปเลย
    created = serializers.DateTimeField(default=timezone.now())  # timezone มันดีกว่า datetime ปกตินะ
    temperature = serializers.DecimalField(max_digits=4, decimal_places=2)  # เขียนเหมือนกับใน model เลยนะ
    o2sat = serializers.IntegerField()
    systolic = serializers.IntegerField()
    diastolic = serializers.IntegerField()
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        # data = {'temperature': 36.5, 'o2sat': 98, 'systolic': 120, 'diastolic': 79, 'user': User.objects.last().id}
        # **data = 'temperature': 36.5, 'o2sat': 98, 'systolic': 120, 'diastolic': 79, 'user': User.objects.last().id
        return Measurement.objects.create(**validated_data)