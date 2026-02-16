from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.director_dashboard, name='director_dashboard'),
    path('employee/', views.employee_management, name='employee_management'),
    path('attendance_leave/', views.attendance_leave, name='attendance_leave'),
    path('settings/', views.company_settings, name='company_settings'),
    path('profile/', views.director_profile, name='director_profile'),
    path('notifications/', views.notifications, name='notifications'),

    path('change-password/', views.change_password, name='change_password'),
    path('edit_hr/<int:hr_id>/', views.edit_hr, name='edit_hr'),

    path('view-hrs/', views.view_hrs, name='view_hrs'),
    path('assign-hr-tasks/', views.assign_hr_tasks, name='assign_hr_tasks'),
    path('edit-staff/<int:staff_id>/', views.director_edit_staff, name='director_edit_staff'),
    path('suspend/hr/<int:hr_id>/', views.suspend_hr, name='suspend_hr'),
    path('suspend/manager/<int:manager_id>/', views.suspend_manager, name='suspend_manager'),
    path('suspend/staff/<int:staff_id>/', views.suspend_staff, name='suspend_staff'),

]
