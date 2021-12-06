from django.http import HttpResponse

from . import models


def current_temperature(request):
    return HttpResponse(f'Temperature: {models.Measurement.objects.last().temperature}')  # เป็นการดึงค่า temperature ที่เป็น last() ออกมาจาก db นะ
