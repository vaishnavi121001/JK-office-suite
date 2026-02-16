# manager_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('leaves/', views.leave_tracker, name='leave_tracker'),
    path('review/', views.review_staff, name='review_staff'),
    path('message/', views.send_message, name='send_message'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('profile/', views.profile, name='profile'),
    path('view-staff-list/', views.view_staff_list, name='view_staff_list'),
   path('tasks/', views.view_tasks, name='view_tasks'),
    path('tasks/assign/<int:staff_id>/', views.assign_task, name='assign_task'),

    path('task-list/', views.task_list, name='task_list'),
    path('staff-list/', views.staff_list_for_assignment, name='staff_list_for_assignment'),
    path('staff/view/<int:staff_id>/', views.manager_view_staff, name='manager_view_staff'),
    path('staff/edit/<int:staff_id>/', views.manager_edit_staff, name='manager_edit_staff'),
    path('payroll/', views.view_payroll, name='view_payroll'),
    path('leave/<int:leave_id>/manage/', views.manage_leave_status, name='manage_leave_status'),

]
