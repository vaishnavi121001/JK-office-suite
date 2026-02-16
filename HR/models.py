# staff/models.py
from django.db import models
from django.urls import reverse
from django.utils import timezone
from Authentication.models import Staff, Manager

# --- Constants ---
EMPLOYMENT_TYPES = (
    ('Full-Time', 'Full-Time'),
    ('Part-Time', 'Part-Time'),
    ('Internship', 'Internship'),
    ('Contract', 'Contract'),
)

STATUS_CHOICES = (
    ('Open', 'Open'),
    ('Closed', 'Closed'),
)

# --- RecruitmentPost Model ---
class RecruitmentPost(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    hiring_manager = models.CharField(max_length=100)
    vacancies = models.PositiveIntegerField()
    job_description = models.TextField()
    requirements = models.TextField()
    experience_required = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    location = models.CharField(max_length=100)
    posted_date = models.DateField(auto_now_add=True)
    last_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    is_locked = models.BooleanField(default=False)
    offer_letter = models.FileField(upload_to='offer_letters/', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('recruitment_detail', args=[str(self.pk)])

# --- Salary Model ---
class Salary(models.Model):
    EMPLOYEE_TYPE_CHOICES = [
        ('staff', 'Staff'),
        ('manager', 'Manager'),
    ]

    employee_type = models.CharField(max_length=10, choices=EMPLOYEE_TYPE_CHOICES)

    staff = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='salary_records_as_staff'  # ✅ related_name दिया
    )
    manager = models.ForeignKey(
        Manager,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='salary_records_as_manager'  # ✅ related_name दिया
    )

    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    hra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ta = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    is_locked = models.BooleanField(default=False)
    payslip = models.FileField(upload_to='payslips/', null=True, blank=True)

    def __str__(self):
        return self.get_employee_name()

    def get_employee_name(self):
        if self.employee_type == 'staff' and self.staff:
            return self.staff.full_name
        elif self.employee_type == 'manager' and self.manager:
            return self.manager.full_name
        return "Unknown"

    def get_employee_department(self):
        if self.employee_type == 'staff' and self.staff:
            return self.staff.department
        elif self.employee_type == 'manager' and self.manager:
            return self.manager.department
        return "N/A"

    def get_employee_designation(self):
        if self.employee_type == 'staff' and self.staff:
            return self.staff.designation
        elif self.employee_type == 'manager' and self.manager:
            return self.manager.designation
        return "N/A"
