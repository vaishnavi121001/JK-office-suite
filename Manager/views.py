from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth import logout

from Authentication.forms import StaffRegistrationForm
from .forms import *
from .models import Attendance, LeaveApplication, PerformanceReview, Notification, Payroll
from Staff.models import Task
from Authentication.models import Manager, Staff


@login_required
def manager_dashboard(request):
    manager_id = request.session.get('user_id')
    if not manager_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')

    manager = get_object_or_404(Manager, id=manager_id)
    staff_list = Staff.objects.filter(manager=manager)
    total_staff = staff_list.count()

    today = now().date()
    today_attendance = Attendance.objects.filter(staff__manager=manager, date=today).count()
    pending_leaves = LeaveApplication.objects.filter(staff__manager=manager, status='Pending').count()

    context = {
        'manager': manager,
        'staff_list': staff_list,
        'attendance_records': Attendance.objects.filter(staff__manager=manager).order_by('-date')[:5],
        'leave_applications': LeaveApplication.objects.filter(staff__manager=manager).order_by('-applied_on')[:5],
        'performance_reviews': PerformanceReview.objects.filter(staff__manager=manager),
        'total_staff': total_staff,
        'today_attendance': today_attendance,
        'pending_leaves': pending_leaves,
    }
    return render(request, 'manager/dashboard.html', context)


@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance marked successfully.")
            return redirect('manager_dashboard')
    else:
        form = AttendanceForm()
    return render(request, 'manager/mark_attendance.html', {'form': form})


@login_required
def leave_tracker(request):
    manager_id = request.session.get('user_id')
    manager = get_object_or_404(Manager, id=manager_id)
    leaves = LeaveApplication.objects.filter(staff__manager=manager).order_by('-applied_on')
    return render(request, 'manager/leave.html', {'leaves': leaves})


@login_required
def manage_leave_status(request, leave_id):
    leave = get_object_or_404(LeaveApplication, id=leave_id)

    if request.method == 'POST' and leave.status == 'Pending':
        action = request.POST.get('action')
        if action == 'approve':
            leave.status = 'Approved'
        elif action == 'reject':
            leave.status = 'Rejected'
        leave.save()

        Notification.objects.create(
            user_type='staff',
            user_id=leave.staff.id,
            message=f"Your leave request from {leave.start_date} to {leave.end_date} was {leave.status}."
        )
        messages.success(request, f"Leave has been {leave.status.lower()} successfully.")
    else:
        messages.info(request, "Leave request already processed or invalid request.")

    return redirect('leave_tracker')


from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import PerformanceReviewForm
from .models import Staff

@login_required
def review_staff(request):
    # Make sure to filter the staff members based on the logged-in user's company code
    staff_member = Staff.objects.get(user=request.user)  # Assuming the 'user' is related to Staff

    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            # Create performance review instance, setting staff and reviewer automatically
            performance_review = form.save(commit=False)
            performance_review.staff = staff_member  # Automatically assign the logged-in user as staff
            performance_review.reviewer = request.user  # Logged-in user is the reviewer
            performance_review.save()

            messages.success(request, "Performance review submitted successfully.")
            return redirect('manager_dashboard')  # Adjust according to your URL

    else:
        form = PerformanceReviewForm()

    return render(request, 'manager/review.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Message, Manager, Staff
from .forms import MessageForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid():
            # Ensure the logged-in user is a Manager
            if isinstance(request.user, Manager):  # Check if the user is a Manager
                manager = request.user  # Use the logged-in Manager instance
            else:
                # If the user is not a Manager, redirect or handle the error
                messages.error(request, "You must be a manager to send messages.")
                return redirect('manager_dashboard')  # Or redirect to an appropriate page

            # Create a new message instance, setting the sender as the Manager
            message = form.save(commit=False)
            message.sender = manager  # Assign the Manager as the sender
            message.save()

            messages.success(request, "Message sent successfully.")
            return redirect('manager_dashboard')
    else:
        form = MessageForm()

    return render(request, 'manager/message.html', {'form': form})


@login_required
def view_notifications(request):
    manager_id = request.session.get('user_id')
    notes = Notification.objects.filter(user_type='manager', user_id=manager_id)
    return render(request, 'manager/notifications.html', {'notifications': notes})


@login_required
def profile(request):
    manager = get_object_or_404(Manager, id=request.session.get('user_id'))
    if request.method == 'POST':
        form = ManagerProfileForm(request.POST, instance=manager)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ManagerProfileForm(instance=manager)
    return render(request, 'manager/profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            manager = get_object_or_404(Manager, id=request.session.get('user_id'))
            user = manager.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, "Password changed successfully.")
            logout(request)
            return redirect('login')
    else:
        form = ChangePasswordForm()
    return render(request, 'manager/change_password.html', {'form': form})


@login_required
def staff_list_for_assignment(request):
    manager = get_object_or_404(Manager, id=request.session.get('user_id'))
    staff_members = Staff.objects.filter(manager=manager)
    return render(request, 'manager/staff_list_for_assignment.html', {'staff_members': staff_members})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import TaskAssignForm


@login_required
def assign_task(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    if request.method == 'POST':
        form = TaskAssignForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.staff = staff
            task.save()
            messages.success(request, "Task assigned successfully.")
            return redirect('staff_list_for_assignment')
        else:
            print(form.errors)  # For debugging
    else:
        form = TaskAssignForm()

    return render(request, 'manager/assign_task.html', {'form': form, 'staff': staff})


@login_required
def view_tasks(request):
    manager = get_object_or_404(Manager, id=request.session.get('user_id'))
    tasks = Task.objects.filter(staff__manager=manager).order_by('-due_date')
    return render(request, 'manager/view_tasks.html', {'tasks': tasks})


@login_required
def task_list(request):
    manager = get_object_or_404(Manager, id=request.session.get('user_id'))
    staff_members = Staff.objects.filter(manager=manager)
    tasks = Task.objects.filter(staff__in=staff_members).order_by('-created_at')
    return render(request, 'manager/task_list.html', {'tasks': tasks, 'manager': manager})




@login_required
def view_payroll(request):
    payrolls = Payroll.objects.all()
    return render(request, 'manager/payroll.html', {'payrolls': payrolls})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Staff, Manager


@login_required
def view_staff_list(request):
    manager_id = request.session.get('user_id')
    if not manager_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('login')

    manager = get_object_or_404(Manager, id=manager_id)
    staff_list = Staff.objects.filter(manager=manager)
    return render(request, 'manager/staff_list.html', {'staff_list': staff_list})


@login_required
def manager_view_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    return render(request, 'manager/staff_detail.html', {'staff': staff})


@login_required
def manager_edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('staff_overview')
    else:
        form = StaffRegistrationForm(instance=staff)
    return render(request, 'manager/edit_staff.html', {'form': form, 'staff': staff})
