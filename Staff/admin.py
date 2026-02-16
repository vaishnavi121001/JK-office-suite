from django.contrib import admin
from .models import Staff, Task
from django.utils.html import format_html


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'staff', 'status', 'due_date', 'start_time', 'end_time', 'created_at')
    list_filter = ('status', 'staff')
    search_fields = ('title', 'staff__full_name')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        # You can add custom logic here to update or modify fields before saving the task.
        super().save_model(request, obj, form, change)

    def status_tag(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            'green' if obj.status == 'Completed' else 'red',
            obj.status
        )

    status_tag.short_description = 'Status'



admin.site.register(Task, TaskAdmin)
