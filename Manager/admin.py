from django.contrib import admin
from .models import Attendance, LeaveApplication, PerformanceReview, Payroll, Message, Notification

from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('staff', 'date',)
    search_fields = ('staff__full_name', 'staff__email')  # Customize if needed
    ordering = ('-date',)


@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_date', 'end_date', 'status', 'applied_on')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('staff__full_name', 'reason')
    ordering = ('-applied_on',)


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('staff', 'review_date', 'score', 'comments')
    list_filter = ('review_date', 'score')
    search_fields = ('staff__full_name', 'comments')
    ordering = ('-review_date',)


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('staff', 'month', 'year', 'salary_paid', 'processed_on')
    list_filter = ('month', 'year')
    search_fields = ('staff__full_name', 'month', 'year')
    ordering = ('-processed_on',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'sent_at', 'read')
    list_filter = ('read', 'sent_at')
    search_fields = ('sender__full_name', 'receiver__full_name', 'message')
    ordering = ('-sent_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'user_id', 'message', 'is_read', 'created_at')
    list_filter = ('user_type', 'is_read', 'created_at')
    search_fields = ('message',)
    ordering = ('-created_at',)
