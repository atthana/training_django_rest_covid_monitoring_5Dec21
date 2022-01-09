from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import Measurement, Symptom

User = get_user_model()


# ถ้าอยากเห็น detail อะไรเพิ่ม ก็ทำ serializer ของตัวนั้นขึ้นมา

class UserSerializer(serializers.ModelSerializer):  # อยากเห็น detail ของอะไรเพิ่ม ก้อทำ serializer ของคนนั้นขึ้นมา
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']
        # fields = '__all__'  ถ้าเอา all นะ พวก password มันจะไปด้วยนี่สิ


class SymptomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Symptom
        fields = '__all__'


class MeasurementSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(default=timezone.now())
    symptoms = SymptomSerializer(many=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              default=serializers.CurrentUserDefault())

    # ============= พวกนี้ทำเพิ่ม ตอนที่อ.สอน เพื่อให้เข้าใจมากขึ้นนะ ทั้งชุดนี้เลยในการ override output ที่จะพ่นออกไป ====================
    # user = UserSerializer()  # ในนี้ที่จะพ่นออกไป เราก้อ override ไปเลย
    # first_name = serializers.CharField(source='user.first_name', read_only=True)  # ใช้แบบนี้ก็ได้นะ เราสามารถแทรก field อะไรเข้าไปก็ได้นะ
    # full_name = serializers.SerializerMethodField()
    # แต่ field ที่เขียนแบบนี้จะเป็น read-only นะ หมายความว่าจะโชว์เฉพาะตอนที่เปลี่ยนจาก object เป็น json เท่านั้น

    # symptoms ตรงนี้เราจะ serialize มันออกไปอย่างไร ก็เอามาจาก SymptomSerializer ไง
    # เป็นการ serialize ตัว many to many ออกมา แล้วได้ทั้ง key และ value ออกมา

    # def get_full_name(self, obj):
    #     return f"{obj.user.first_name} {obj.user.last_name}"

    class Meta:
        model = Measurement
        fields = '__all__'

    def create(self, validated_data):
        symptoms = validated_data.pop('symptoms')  # ดึง symptoms ออกมาข้างนอกก่อน ไม่สนใจมัน
        measurement = Measurement.objects.create(**validated_data)
        measurement.symptoms.set(Symptom.objects.filter(id__in=[s['id'] for s in symptoms]))
        # แล้วค่อยไป set symptoms เข้าไปทีหลังอีกที
        # set() ใช้สำหรับ add ค่าให้กับ many to many field
        return measurement

    def update(self, instance, validated_data):
        symptoms = validated_data.pop('symptoms')
        measurement = super().update(instance, validated_data)
        measurement.symptoms.set(Symptom.objects.filter(id__in=[s['id'] for s in symptoms]))
        return measurement
