from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index,name='ultimate_home'),
    path('accounts/login/', views.user_login,name='login2'),
    path('accounts/logout/', views.user_logout,name='logout2'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/login.html')),
    path('accounts/profile/', views.profile),    
    path(
        'accounts/change-password/',
        auth_views.PasswordChangeView.as_view(success_url='/'),
        name='change_password'
    ),
    path('admin/login/',views.index, name='password_change_done'),
    path('admin/import/', views.import_user, name='admin_import'),


]
