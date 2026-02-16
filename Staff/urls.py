
from django.urls import path
from . import views

urlpatterns = [

    path('view-secret-key/', views.view_secret_key, name='view_secret_key'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('profile/', views.staff_profile, name='staff_profile'),
    path('notifications/', views.staff_notifications, name='staff_notifications'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('profile/', views.staff_profile, name='staff_profile'),
    path('notifications/', views.staff_notifications, name='staff_notifications'),
    path('tasks/', views.staff_tasks, name='staff_tasks'),
    path('attendance/', views.staff_attendance, name='staff_attendance'),
    path('leave/', views.staff_leave, name='staff_leave'),
    path('messages/', views.staff_messages, name='staff_messages'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path('send_message/', views.message, name='message'),
    path('staff/qr-code/', views.staff_dashboard, name='staff_qr_code'),
    path('leave/status/', views.staff_leave_status, name='staff_leave_status'),
    path('tasks/update/<int:task_id>/', views.update_task, name='update_task'),
path('check-tasks-and-logout/', views.check_tasks_and_logout, name='check_tasks_and_logout'),
]
