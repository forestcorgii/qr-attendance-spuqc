
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('qr_attendance_app.urls')),
    path('finance/', include('finance_app.urls')),
    path('student/', include('student_app.urls')),
    path('office/', include('office_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
