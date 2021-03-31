from django.urls import path, include, re_path
from . import views

# from student_app import models as studentModels

from django.contrib.auth import views as auth_views


# from rest_framework import serializers 

# class AttendanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = studentModels.Attendance
#         fields = ['']


urlpatterns = [
    path('Scan/',views.Scan,name='scan_event'),
    path('',views.home),
    path('profile/', views.profile),
    

    # path('events/edit/<int:pk>/',views.edit,name='edit_event'),
    path('events/delete/<int:pk>/',views.delete,name='delete_event'),
    path('events/<int:pk>/',views.detail,name='event_detail'),    
    path('events/',views.event,name='event'),
]
