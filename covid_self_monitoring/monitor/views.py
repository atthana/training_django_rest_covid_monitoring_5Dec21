import json

from django.http import HttpResponse

from . import models


def current_temperature(request):
    data = {'temperature': str(models.Measurement.objects.last().temperature)}  # อันนี้เพราะ temp มันเป็น decimal field นะ จึงต้องแปลงให้เป็น String ก่อน
    return HttpResponse(json.dumps(data))

