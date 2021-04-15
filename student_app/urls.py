from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='student_home'),
    path('qr', views.qr_generator, name='qr_generator'),
    path('clearances/', views.clearances, name='student_clearances'),
    path('clearances/request/<int:pk>/', views.request_clearance, name='request_clearance'),
]