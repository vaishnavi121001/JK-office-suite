from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('employee/', views.employee_panel, name='employee_panel'),
    path('manage/', views.manage_employees, name='manage_employees'),
    path('profile/', views.hr_profile, name='hr_profile'),

    path('manage/', views.manage_employees, name='manage_employees'),
    path('recruitment/', views.recruitment_list, name='recruitment_list'),
    path('recruitment/add/', views.add_recruitment, name='add_recruitment'),
    path('recruitment/edit/<int:post_id>/', views.edit_recruitment, name='edit_recruitment'),
    path('recruitment/delete/<int:post_id>/', views.delete_recruitment, name='delete_recruitment'),
    path('recruitment/lock/<int:post_id>/', views.lock_recruitment, name='lock_recruitment'),
    path('recruitment/upload_offer_letter/<int:post_id>/', views.upload_offer_letter, name='upload_offer_letter'),
    path('download/csv/', views.download_recruitment_csv, name='download_recruitment_csv'),
    path('download/pdf/', views.download_recruitment_pdf, name='download_recruitment_pdf'),
    path('recruitment/export/', views.export_recruitment, name='export_recruitment'),
    path('recruitment/<int:pk>/', views.recruitment_detail, name='recruitment_detail'),
    path('manage-employees/', views.manage_employees, name='manage_employees'),
    path('assign-manager/<int:staff_id>/', views.assign_manager, name='assign_manager'),
    path('edit-staff/<int:staff_id>/', views.edit_staff, name='edit_staff'),

    path('edit-manager/<int:manager_id>/', views.edit_manager, name='edit_manager'),

    path('manual-shuffle/', views.manual_team_shuffle, name='manual_team_shuffle'),
    path('save-shuffling/', views.save_team_shuffling, name='save_team_shuffling'),
    path('dashboard/salary_list', views.salary_list, name='salary_list'),
    path('dashboard/add_salary/', views.add_salary, name='add_salary'),
    path('salary/slip/<int:salary_id>/', views.download_payslip, name='download_payslip'),

]
