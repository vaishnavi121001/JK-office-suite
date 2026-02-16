from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random, string


# -- Company Model --
class Company(models.Model):
    company_name = models.CharField(max_length=255)
    company_email = models.EmailField(unique=True)
    company_phone = models.CharField(max_length=20)
    address = models.TextField()
    company_code = models.CharField(max_length=10, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name


# -- Director Model --
class Director(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    adhar_card = models.CharField(max_length=12, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, blank=True)
    company_code = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    emergency_phone = models.CharField(max_length=15)
    address = models.TextField()
    qualifications = models.TextField()
    experience = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = self.generate_password()
        super().save(*args, **kwargs)

    def generate_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

    def __str__(self):
        return f"{self.full_name} ({self.username})"


# -- HR Model --
class HR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    adhar_card = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    company_code = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    emergency_phone = models.CharField(max_length=20)
    address = models.TextField()
    qualifications = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to User model
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    adhar_card = models.CharField(max_length=12, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    company_code = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()
    salary = models.DecimalField(null=True, max_digits=10, decimal_places=2, default=0)
    emergency_phone = models.CharField(max_length=15)
    address = models.TextField()
    qualifications = models.TextField()
    experience = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} ({self.username})"


# -- Staff Model --
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20)
    adhar_card = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    company_code = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100)
    joining_date = models.DateField(default=timezone.now)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    emergency_phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    qualifications = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=255, blank=True, null=True)
    qr_code = models.ImageField(upload_to='staff_qr_codes/', blank=True, null=True)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

    @property
    def has_manager(self):
        return self.manager is not None
