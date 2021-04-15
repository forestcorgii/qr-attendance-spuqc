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
     path('',views.home),
]
