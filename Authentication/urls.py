# authentication/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/staff/', views.staff_register, name='staff_register'),
    path('', views.company_register, name='company_register'),
    path('login/', views.login_view, name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('director/register/', views.director_register, name='director_register'),
    path('hr/register/', views.hr_register, name='hr_register'),
    path('manager/register/', views.manager_register, name='manager_register'),

]
