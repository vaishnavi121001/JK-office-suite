from django.contrib import admin
from .models import Company, Director, HR, Manager, Staff


# Company Admin
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_email', 'company_phone', 'company_code', 'created_at')
    search_fields = ('company_name', 'company_email', 'company_code')
    list_filter = ('created_at',)


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'contact_number', 'username', 'company_code', 'joining_date', 'salary', 'show_password')
    search_fields = ('full_name', 'email', 'username', 'company_code')
    list_filter = ('joining_date',)

    def show_password(self, obj):
        return obj.password

    show_password.short_description = 'Password'


# HR Admin
@admin.register(HR)
class HRAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'contact_number', 'username', 'password', 'company_code', 'department', 'joining_date',
        'salary')
    search_fields = ('full_name', 'email', 'username', 'company_code', 'department')
    list_filter = ('department', 'joining_date')


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'full_name', 'email', 'contact_number', 'adhar_card', 'username', 'password',
        'company_code', 'department', 'joining_date', 'salary', 'emergency_phone',
        'address', 'qualifications', 'experience', 'created_at'
    ]
    search_fields = ['full_name', 'email', 'username', 'department']
    list_filter = ['department', 'joining_date', 'company_code']


# Staff Admin
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'full_name', 'email', 'contact_number', 'username', 'password', 'company_code', 'department', 'position',
        'joining_date',
        'salary')
    search_fields = ('full_name', 'email', 'username', 'company_code', 'department', 'position')
    list_filter = ('department', 'joining_date')
