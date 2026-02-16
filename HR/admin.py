from django.contrib import admin
from .models import RecruitmentPost
from django.contrib import admin
from .models import Salary
admin.site.register(RecruitmentPost)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('get_employee_name', 'employee_type', 'net_salary', 'payment_date', 'is_locked')
    list_filter = ('employee_type', 'is_locked', 'payment_date')
    search_fields = ('staff__full_name', 'manager__full_name')
