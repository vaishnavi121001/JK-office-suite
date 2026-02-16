# manager_app/models.py
from django.contrib.auth.models import User
from django.db import models
from Staff.models import Staff
from Authentication.models import Manager
from django.utils import timezone

from django.contrib.auth.models import User
from django.db import models
from Staff.models import Staff
from django.utils import timezone

# Other models remain the same as before...

from django.db import models
from django.utils import timezone
from django.db import models
from django.utils.timezone import now
import hashlib


def generate_secret_key():
    today = now().date()
    return hashlib.sha256(f"defaultuser{today}".encode()).hexdigest()[:8].upper()


class Attendance(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)  # NEW
    date = models.DateField(default=now)
    status = models.CharField(max_length=10, choices=[
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Leave', 'Leave'),
        ('Half-Day', 'Half-Day'),
    ])
    secret_key_used = models.CharField(max_length=100, default=generate_secret_key)

    class Meta:
        unique_together = ('staff', 'date')

    def __str__(self):
        return f"{self.staff.full_name} - {self.date} - {self.status}"


class LeaveApplication(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                              default='pending', max_length=10)
    applied_on = models.DateTimeField(auto_now_add=True)


class PerformanceReview(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    review_date = models.DateField()
    score = models.PositiveIntegerField()
    comments = models.TextField()


class Payroll(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    year = models.IntegerField()
    total_days = models.IntegerField()
    present_days = models.IntegerField()
    salary_paid = models.DecimalField(max_digits=10, decimal_places=2)
    processed_on = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    sender = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class Notification(models.Model):
    user_type = models.CharField(max_length=20)  # manager/staff
    user_id = models.IntegerField(default=1)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
