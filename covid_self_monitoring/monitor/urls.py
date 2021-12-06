from django.urls import path

# เราต้องสร้าง urls แยกของแต่ล่ะ app เพื่อไม่ให้ urls หลักใน project มันใหญ่เกินไปนะ
from . import views

urlpatterns = [
    path('current-temperature/', views.current_temperature),
    path('all-measurement/', views.all_measurement)
]
