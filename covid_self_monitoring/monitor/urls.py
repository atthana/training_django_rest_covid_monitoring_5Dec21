from django.urls import path, include
from . import views

# เราต้องสร้าง urls แยกของแต่ล่ะ app เพื่อไม่ให้ urls หลักใน project มันใหญ่เกินไปนะ
from rest_framework.routers import DefaultRouter

# ถ้าใช้ viewsets, url จะพิศดารกว่าเพื่อนหน่อยนะคือ จะใช้ routers
router = DefaultRouter()
router.register('measurement-viewsets', views.MeasurementViewsets)
router.register('symptom-viewsets', views.SymptomViewsets)

urlpatterns = [
    path('', include(router.urls)),
    path('current-temperature/', views.current_temperature),
    path('all-measurement/', views.all_measurement),
    path('all-measurement-api-view/', views.AllMeasurementView.as_view()),
    # ถ้าเป็น class จะต้องสั่ง as_view() ด้วยนะ สำคัญนะ, ไม่เหมือน function view ที่ใส่ไปเฉยๆนะ

    path('measurement-generics-view/', views.MeasurementGenericsView.as_view()),
    # ต้องมี as_view() ด้วยนะ อย่าลืม เพราะมันเป็น class view.

    path('symptom-generics-view/', views.SymptomGenericsView.as_view()),
    path('symptom-generics-view/<int:id>', views.SymptomGenericsDetailView.as_view())
]
