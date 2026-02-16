from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import HRRegistrationForm, ManagerRegistrationForm, StaffRegistrationForm, CompanyRegistrationForm, DirectorRegistrationForm, LoginForm
from .models import Director, HR, Manager, Staff
from Director.models import Notification

import random
import string
from .utils import generate_password


def generate_company_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_password(full_name, adhar_card):
    name_part = ''.join(full_name.split())[:3].lower()
    adhar_part = adhar_card[-4:]
    return name_part + adhar_part


def company_register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save(commit=False)
            company.company_code = generate_company_code()
            company.save()

            subject = 'Your Company Code - JK Office Suite'
            message = f"Hello {company.company_name},\n\nYour Company Code is: {company.company_code}\n\nThanks for registering!"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [company.company_email])

            messages.success(request, f'Company registered successfully! Code sent to {company.company_email}.')
            return redirect('company_register')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'Authentication/company_register.html', {'form': form})


@login_required
def director_register(request):
    if request.method == 'POST':
        form = DirectorRegistrationForm(request.POST)
        if form.is_valid():
            director = form.save()
            send_mail(
                'Welcome to JK Office Suite',
                f'Hello {director.full_name},\n\nUsername: {director.username}\nPassword: {director.password}\nCompany Code: {director.company_code}',
                settings.EMAIL_HOST_USER,
                [director.email],
            )
            return redirect('director_dashboard')
    else:
        form = DirectorRegistrationForm()
    return render(request, 'Authentication/director_register.html', {'form': form})


@login_required
def hr_register(request):
    if request.method == 'POST':
        form = HRRegistrationForm(request.POST)
        if form.is_valid():
            hr = form.save(commit=False)
            password = generate_password(hr.full_name, hr.adhar_card)
            hr.password = password

            user = User.objects.create_user(
                username=hr.username,
                email=hr.email,
                password=password,
                first_name=hr.full_name.split()[0],
                last_name=' '.join(hr.full_name.split()[1:]),
            )
            hr.HR = HR
            hr.save()

            send_mail(
                'Welcome to JK Office Suite - HR Account',
                f"Hello {hr.full_name},\n\nUsername: {hr.username}\nPassword: {password}\nCompany Code: {hr.company_code}",
                settings.EMAIL_HOST_USER,
                [hr.email],
                fail_silently=False,
            )

            Notification.objects.create(user=request.user, message=f"New HR '{hr.full_name}' registered.")
            messages.success(request, 'HR registered successfully!')
            return redirect('user_login')
    else:
        form = HRRegistrationForm()
    return render(request, 'Authentication/hr_register.html', {'form': form})


@login_required
def manager_register(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            manager = form.save(commit=False)
            password = generate_password(manager.full_name, manager.adhar_card)
            manager.password = password

            user = User.objects.create_user(
                username=manager.username,
                email=manager.email,
                password=password,
                first_name=manager.full_name.split()[0],
                last_name=' '.join(manager.full_name.split()[1:]),
            )

            manager.user = user
            manager.save()

            send_mail(
                'Welcome to JK Office Suite - Manager Account',
                f"Hello {manager.full_name},\n\nUsername: {manager.username}\nPassword: {password}",
                settings.EMAIL_HOST_USER,
                [manager.email],
            )

            Notification.objects.create(user=request.user, message=f"New Manager '{manager.full_name}' registered.")
            return redirect('user_login')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'Authentication/manager_register.html', {'form': form})


def staff_register(request):
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            adhar_card = form.cleaned_data['adhar_card']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
                return render(request, 'Authentication/staff_register.html', {'form': form})

            password = generate_password(full_name, adhar_card)

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name.split()[0],
                last_name=' '.join(full_name.split()[1:]),
            )

            staff = form.save(commit=False)
            staff.user = user
            staff.password = password
            staff.save()

            subject = 'Welcome to JK Office Suite - Staff Account'
            message = f"Hello {full_name},\n\nYour staff account has been created successfully.\n\nUsername: {username}\nPassword: {password}\n\nYou can now log in to your account."

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )

            messages.success(request, f"Staff registered successfully. Login password: {password}")
            return redirect('user_login')
    else:
        form = StaffRegistrationForm()

    return render(request, 'Authentication/staff_register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user and user.is_superuser:
                login(request, user)
                return redirect('/admin/')
            else:
                messages.error(request, "Invalid admin credentials.")
    else:
        form = LoginForm()

    return render(request, 'Authentication/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect('home')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'Authentication/password_reset.html'
    email_template_name = 'Authentication/password_reset_email.html'
    subject_template_name = 'Authentication/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'Authentication/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'Authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'Authentication/password_reset_complete.html'


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']

            try:
                director = Director.objects.get(username=uname, password=pwd)
                request.session['user_id'] = director.id
                request.session['role'] = 'director'
                return redirect('director_dashboard')
            except Director.DoesNotExist:
                pass

            try:
                manager = Manager.objects.get(username=uname, password=pwd)
                request.session['user_id'] = manager.id
                request.session['role'] = 'manager'
                return redirect('manager_dashboard')
            except Manager.DoesNotExist:
                pass

            try:
                staff = Staff.objects.get(username=uname, password=pwd)
                request.session['user_id'] = staff.id
                request.session['role'] = 'staff'
                return redirect('staff_dashboard')
            except Staff.DoesNotExist:
                pass

            try:
                hr = HR.objects.get(username=uname, password=pwd)
                request.session['user_id'] = hr.id
                request.session['role'] = 'hr'
                return redirect('hr_dashboard')
            except HR.DoesNotExist:
                pass

            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'Authentication/manager_login.html', {'form': form})
