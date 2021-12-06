import json

from django.http import HttpResponse

from . import models


def current_temperature(request):
    data = {'temperature': str(
        models.Measurement.objects.last().temperature)}  # อันนี้เพราะ temp มันเป็น decimal field นะ จึงต้องแปลงให้เป็น String ก่อน
    return HttpResponse(json.dumps(data))


def all_measurement(request):
    data = list()
    for m in models.Measurement.objects.all():
        data.append({
            'created': str(m.created),
            'user_id': str(m.user.id),
            'temperature': str(m.temperature),
            'o2sat': str(m.o2sat),
            'systolic': str(m.systolic),
            'diastolic': str(m.diastolic),
            'symptoms': m.symptoms_display
        })

    return HttpResponse(json.dumps(data))
