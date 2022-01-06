import json

from django.http import HttpResponse
from rest_framework import generics, viewsets
from rest_framework.decorators import api_view  # ตัวนี้เป็น decorator ใช้สำหรับ Function based views
from rest_framework.response import Response
from rest_framework.views import APIView  # For Class based views.

from . import models
from .models import Measurement, Symptom
from .serializers import MeasurementSerializer, SymptomSerializer


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
        serializer = MeasurementSerializer(Measurement.objects.all(), many=True)  # query ค่า แล้วก้อ serializer ออกไป
        return Response(data=serializer.data)  # พวกนี้จะ return เหมือนกับ api_view ข้างบนเลยนะ


# class MeasurementGenericsView(generics.ListAPIView):  # อันนี้มันคือการ GET ออกมานะ
#     # อย่างที่บอกนะ property ที่มันต้องการ 2 ตัวคือ queryset กับ serializer_class
#     queryset = Measurement.objects.all()  # queryset เพื่อบอกให้รู้ว่าตอนที่มันจะไปสร้าง serializer เนี่ยมันต้อง query อะไรออกมาบ้าง
#     serializer_class = MeasurementSerializer  # ตอนที่มันจะแปลงค่าจาก object ให้กลายเป็น json จะต้องใช้ serializer ตัวไหน
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         qs = qs.filter(id=self.kwargs['pk'])
#         return qs

# class MeasurementGenericsView(generics.RetrieveAPIView):
#     queryset = Measurement.objects.all()
#     serializer_class = MeasurementSerializer
#     lookup_field = 'id'
#     # ใส่ตรงนี้ว่าเราจะไป lookup อะไร ซึ่งคือ pk หรือ primary key นั่นแหละใน db (ใช้ id หรือ pk ก็ได้นะ Django รู้จักหมด)
#     # แต่ถ้าเราไม่ใส่ id มันจะ error นะ เพราะใน url มันบอกว่า required id ด้วย


class MeasurementGenericsView(generics.ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class SymptomGenericsView(generics.ListCreateAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer


class SymptomGenericsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
    lookup_field = 'id'


class MeasurementViewsets(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer  # เขียนแค่นี้เลยนะ เวลาเราเขียน ViewSets


class SymptomViewsets(viewsets.ReadOnlyModelViewSet):  # ต้องใช้ 56, 61 ถึงจะได้เท่ากับอันนี้นะ
    queryset = Symptom.objects.all()
    serializer_class = SymptomSerializer
