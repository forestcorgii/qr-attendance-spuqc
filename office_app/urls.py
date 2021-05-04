from django.urls import path, include, re_path
from . import views

# from student_app import models as studentModels

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('Scan/',views.Scan,name='scan_event'),
    path('',views.home),
    path('profile/', views.profile),
    

    # path('events/edit/<int:pk>/',views.edit,name='edit_event'),
    path('events/', views.event_all, name='event'),
    path('events/<int:pk>/',views.detail,name='event_detail'),    
    path('events/create/', views.create_event, name='create_event'),
    path('events/delete/<int:pk>/',views.delete,name='delete_event'),
    
    path('clearances/', views.clearances, name='office_clearances'),
    path('clearances/approve/<int:pk>', views.approve_clearance, name='approve_clearance'),    
    path('clearances/reject/<int:pk>', views.reject_clearance, name='reject_clearance'),    
    path('clearances/cancel/<int:pk>', views.cancel_clearance_approval, name='cancel_clearance'),    
]
