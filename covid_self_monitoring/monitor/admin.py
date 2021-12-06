from django.contrib import admin
from . import models

# Register ทั้ง 2 models นะ
@admin.register(models.Symptom)
class SymptomAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'temperature',
                    'o2sat', 'systolic', 'diastolic', 'symptoms_display']
    # symptoms_diaplay มันคือ ตัวที่อยู่ใน @property นั่นแหละใน models.py ที่ได้เราสร้างไว้ก่อนหน้านี้
    # ชื่อของ fileds ต่างๆที่จะเอามาโชว์ จะต้องพิมพ์ให้ถูกด้วยนะ ต้องเป๊ะ
    # พวก list พวกนี้มันมีใน Django หมดแล้ว กำหนดได้ว่าจะให้โชว์อะไรบ้าง
    list_filter = ['user', 'created']
    # พวกนี้คือเราต้องการให้ filter จากด้านข้างได้ด้วย โดยให้ filter ได้จาก 2 fields นะ
    filter_horizontal = ['symptoms']
    # filter_horizontal ทำให้มัน filter ได้ง่ายขึ้น
