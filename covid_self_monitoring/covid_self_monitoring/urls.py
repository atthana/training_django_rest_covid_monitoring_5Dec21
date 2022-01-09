from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Covid Self Monitoring API",
        default_version='v1',
        description="bla bla..",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # ไม่จำเป็นต้องมี permissions อะไรก็เข้ามาใช้งานได้เลย
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),

    path('admin/', admin.site.urls),
    path('monitor/', include('monitor.urls')),

    # มาสร้าง part เกี่ยวกับ jwt ที่ url ตัวนอกสุดเลยนะ (ไม่ได้อยู่ใน App)
    path('api-token-auth/', jwt_views.TokenObtainPairView.as_view()),  # Part สำหรับทำ authen
    path('api-token-refresh/', jwt_views.TokenRefreshView.as_view())  # Part สำหรับทำ refresh
]
