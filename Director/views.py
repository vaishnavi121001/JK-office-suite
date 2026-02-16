from Authentication.models import Company, Director, HR, Manager, Staff
from Authentication.forms import CompanyRegistrationForm, StaffRegistrationForm, ManagerRegistrationForm, \
    HRRegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from .models import Notification
from .forms import CustomPasswordChangeForm


@login_required
def director_dashboard(request):
    director_id = request.session.get('user_id')
    if not director_id:
        return redirect('login')
    try:
        director = Director.objects.get(id=director_id)
    except Director.DoesNotExist:
        return render(request, 'manager/error.html', {'message': 'Director not found.'})

    company_code = director.company_code
    total_hrs = HR.objects.filter(company_code=company_code).count()
    total_managers = Manager.objects.filter(company_code=company_code).count()
    total_staffs = Staff.objects.filter(company_code=company_code).count()
    total_employees = total_hrs + total_managers + total_staffs

    context = {
        'total_employees': total_employees,
        'total_hrs': total_hrs,
        'total_managers': total_managers,
        'total_staffs': total_staffs,
    }

    return render(request, 'director/dashboard.html', context)


@login_required
def manage_employees(request):
    staff_query = request.GET.get('q', '')
    manager_query = request.GET.get('mq', '')

    staff_list = Staff.objects.filter(
        Q(full_name__icontains=staff_query) |
        Q(email__icontains=staff_query) |
        Q(department__icontains=staff_query)
    )

    managers = Manager.objects.filter(
        Q(full_name__icontains=manager_query) |
        Q(email__icontains=manager_query) |
        Q(department__icontains=manager_query)
    )

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        manager_id = request.POST.get('manager_id')

        try:
            staff = get_object_or_404(Staff, id=staff_id)
            manager = get_object_or_404(Manager, id=manager_id)
            if manager.department == staff.department:
                staff.manager = manager
                staff.save()
                messages.success(request, f"{staff.full_name} has been assigned to {manager.full_name} ✅")
            else:
                messages.error(request, "❌ Manager and Staff must belong to the same department.")
        except Exception as e:
            messages.error(request, f"⚠️ Error: {e}")

    context = {
        'staff_list': staff_list,
        'managers': managers,
        'staff_query': staff_query,
        'manager_query': manager_query,
    }
    return render(request, 'hr/manage_employees.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from Authentication.models import Director, HR, Manager, Staff


@login_required
def employee_management(request):
    director_id = request.session.get('user_id')
    director = get_object_or_404(Director, id=director_id)
    company_code = director.company_code

    hrs = HR.objects.filter(company_code=company_code, is_suspended=False)
    managers = Manager.objects.filter(company_code=company_code, is_suspended=False)
    staffs = Staff.objects.filter(company_code=company_code, is_suspended=False)

    context = {
        'hrs': hrs,
        'managers': managers,
        'staffs': staffs,
    }
    return render(request, 'Director/employee_management.html', context)


@login_required
def company_settings(request):
    try:
        director_id = request.session.get('user_id')
        director = Director.objects.get(id=director_id)
        company = Company.objects.get(company_code=director.company_code)
    except (Director.DoesNotExist, Company.DoesNotExist):
        company = None

    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('director_dashboard')
    else:
        form = CompanyRegistrationForm(instance=company)

    return render(request, 'Director/company_setting.html', {'form': form})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Manager.models import Attendance, LeaveApplication, PerformanceReview


@login_required
def attendance_leave(request):
    # Fetch all attendance records, including related staff
    attendance_data = Attendance.objects.select_related('staff').order_by('-date')

    # Fetch all leave applications
    leave_requests = LeaveApplication.objects.select_related('staff').order_by('-applied_on')

    context = {
        'attendance_records': attendance_data,
        'leave_applications': leave_requests,
    }
    return render(request, 'director/attendance_leave.html', context)


@login_required
def director_profile(request):
    try:
        director_id = request.session.get('user_id')
        director = Director.objects.get(id=director_id)
    except Director.DoesNotExist:
        director = None

    return render(request, 'director/profile.html', {'director': director})


@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'director/notifications.html', {'notifications': notifications})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors.')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'director/change_password.html', {'form': form})


def edit_hr(request, hr_id):
    hr = get_object_or_404(HR, id=hr_id)
    if request.method == 'POST':
        form = HRRegistrationForm(request.POST, instance=hr)
        if form.is_valid():
            form.save()
            return redirect('employee_management')
    else:
        form = HRRegistrationForm(instance=hr)
    context = {'form': form, 'hr': hr}
    return render(request, 'Director/edit_hr.html', context)


@login_required
def view_hrs(request):
    try:
        director_id = request.session.get('user_id')
        director = Director.objects.get(id=director_id)
        hrs = HR.objects.filter(company_code=director.company_code)
        directors = Director.objects.filter(company_code=director.company_code)
        return render(request, 'director/view_hrs.html', {
            'hrs': hrs,
            'directors': directors
        })
    except Director.DoesNotExist:
        messages.error(request, 'Director not found. Please log in again.')
        return redirect('login')


def assign_hr_tasks(request):
    return render(request, 'director/assign_hr_tasks.html')


def director_edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff updated successfully!')
            return redirect('employee_management')
    else:
        form = StaffRegistrationForm(instance=staff)
    return render(request, 'director/director_edit_staff.html', {'form': form, 'staff': staff})


def suspend_hr(request, hr_id):
    hr = get_object_or_404(HR, id=hr_id)

    if request.method == 'POST':
        hr.is_suspended = True
        hr.save()
        messages.success(request, 'HR suspended successfully.')
        return redirect('employee_management')

    return render(request, 'Director/confirm_suspend_hr.html', {'hr': hr})


def suspend_manager(request, manager_id):
    manager = get_object_or_404(Manager, id=manager_id)

    if request.method == 'POST':
        manager.is_suspended = True
        manager.save()
        messages.success(request, 'Manager suspended successfully.')
        return redirect('employee_management')

    return render(request, 'director/confirm_suspend_manager.html', {'manager': manager})


def suspend_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        staff.is_suspended = True
        staff.save()
        messages.success(request, 'Staff suspended successfully.')
        return redirect('employee_management')

    return render(request, 'director/confirm_suspend_staff.html', {'staff': staff})
