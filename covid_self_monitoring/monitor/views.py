import json
from django.http import HttpResponse
from . import models

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Measurement
from .serializers import MeasurementSerializer


def current_temperature(request):
    data = {'temperature': str(
        models.Measurement.objects.last().temperature)}
    return HttpResponse(json.dumps(data))


@api_view(['GET'])
def all_measurement(request):
    serializer = MeasurementSerializer(Measurement.objects.all(), many=True)
    return Response(data=serializer.data)