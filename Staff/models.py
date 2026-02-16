from datetime import timedelta
from django.db import models
from django.utils import timezone

from Authentication.models import Staff

TASK_STATUS_CHOICES = [
    ('Task Given', 'Task Given'),
    ('In Progress', 'In Progress'),
    ('Stuck in Error', 'Stuck in Error'),
    ('Completed', 'Completed'),
]


# Function to provide default end_time
def default_end_time():
    return timezone.now() + timedelta(hours=6)


class Task(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=TASK_STATUS_CHOICES)
    due_date = models.DateField(default=timezone.now)  # today by default
    start_time = models.DateTimeField(default=timezone.now)  # current time
    end_time = models.DateTimeField(default=default_end_time)  # 1 hour from now (fixed)
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    screenshot = models.ImageField(upload_to='task_screenshots/', null=True, blank=True)

    def __str__(self):
        return self.title


class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Completed', 'Completed'), ('Not Completed', 'Not Completed')])
    screenshot = models.ImageField(upload_to='task_screenshots/', blank=True, null=True)
    remarks = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
