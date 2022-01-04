import json
from django.http import HttpResponse
from . import models

from rest_framework.response import Response
from rest_framework.decorators import api_view  # ตัวนี้เป็น decorator ใช้สำหรับ Function based views
from rest_framework.views import APIView  # For Class based views.

from .models import Measurement
from .serializers import MeasurementSerializer


def current_temperature(request):
    data = {'temperature': str(
        models.Measurement.objects.last().temperature)}
    return HttpResponse(json.dumps(data))  # อันนี้คือ response ตัวแรกของ Django เลยแบบ Simple ที่สุด


@api_view(['GET'])
def all_measurement(request):
    serializer = MeasurementSerializer(Measurement.objects.all(), many=True)
    return Response(data=serializer.data)  # ถัดไป response แบบนี้จะใช้กับ Function Based Views


# หลังจากนี้ไป เราจะใช้ Response ของ rest_framework ทั้งหมดนะ
class AllMeasurementView(APIView):
    def get(self, request):  # APIView ข้างบน มันจะมี get นะ
        serializer = MeasurementSerializer(Measurement.objects.all(), many=True)
        return Response(data=serializer.data)  # พวกนี้จะ return เหมือนกับ api_view ข้างบนเลยนะ
