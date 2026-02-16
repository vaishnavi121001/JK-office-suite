from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from Manager.models import Attendance, Message, LeaveApplication, Notification
from Staff.models import Staff, Task, TaskSubmission
from Manager.forms import StaffLeaveApplicationForm, MessageForm, TaskUpdateForm
from datetime import date
import hashlib
import qrcode
import base64
from io import BytesIO
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import json


@login_required
def view_secret_key(request):
    staff = request.user
    today = date.today()
    secret_key = hashlib.sha256((staff.username + str(today)).encode()).hexdigest()[:8].upper()
    return render(request, 'staff/secrete_key.html', {'secret_key': secret_key})


@login_required
def staff_dashboard(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)
    tasks = Task.objects.filter(staff=staff).order_by('-due_date')
    notifications = Notification.objects.all().order_by('-created_at')

    qr_data = json.dumps({
        "username": staff.username,
        "secret_key": hashlib.sha256((staff.username + str(date.today())).encode()).hexdigest()[:8].upper()
    })

    qr = qrcode.make(qr_data)
    qr_image = BytesIO()
    qr.save(qr_image, format='PNG')
    qr_image.seek(0)
    qr_base64 = base64.b64encode(qr_image.getvalue()).decode()

    return render(request, 'staff/dashboard.html', {
        'staff': staff,
        'tasks': tasks,
        'notifications': notifications,
        'qr_base64': qr_base64,
    })


@csrf_exempt
def mark_attendance(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            received_key = data.get('secret_key')

            staff = Staff.objects.get(username=username)
            today = timezone.now().date()
            expected_key = hashlib.sha256((staff.username + str(today)).encode()).hexdigest()[:8].upper()

            if received_key != expected_key:
                return JsonResponse({"success": False, "message": "Invalid secret key."})

            if Attendance.objects.filter(staff=staff, date=today).exists():
                return JsonResponse({"success": False, "message": "Attendance already marked for today."})

            Attendance.objects.create(
                staff=staff,
                date=today,
                status="Present"
            )

            return JsonResponse({"success": True, "message": "Attendance marked successfully!"})

        except Staff.DoesNotExist:
            return JsonResponse({"success": False, "message": "Invalid staff username."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})


@login_required
def staff_profile(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)
    return render(request, 'staff/staff_profile.html', {'staff': staff})


@login_required
def staff_notifications(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    notifications = Notification.objects.filter(user_type='staff', user_id=user_id).order_by('-created_at')
    return render(request, 'staff/notifications.html', {'notifications': notifications})


@login_required
def staff_tasks(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)

    # Check if attendance has been submitted today
    today = date.today()
    has_attended = Attendance.objects.filter(staff=staff, date=today).exists()

    if not has_attended:
        messages.warning(request, "You must submit your attendance before viewing tasks.")
        return redirect('staff_dashboard')  # Replace with actual dashboard or attendance page

    tasks = Task.objects.filter(staff=staff).order_by('-due_date')
    return render(request, 'staff/tasks.html', {'tasks': tasks})


@login_required
def staff_attendance(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)
    attendance_records = Attendance.objects.filter(staff=staff).order_by('-date')
    return render(request, 'staff/attendance.html', {'attendance_records': attendance_records})


@login_required
def staff_leave(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)

    if request.method == 'POST':
        form = StaffLeaveApplicationForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.staff = staff
            leave.status = 'Pending'
            leave.save()

            if staff.manager:
                Notification.objects.create(
                    recipient=staff.manager,
                    user_type='manager',
                    user_id=staff.manager.id,
                    message=f"{staff.full_name} applied for leave from {leave.start_date} to {leave.end_date}."
                )

            return redirect('staff_leave_status')
    else:
        form = StaffLeaveApplicationForm()

    return render(request, 'staff/apply_leave.html', {'form': form})


@login_required
def staff_messages(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)
    messages_list = Message.objects.filter(receiver=staff).order_by('-sent_at')
    return render(request, 'staff/messages.html', {'messages': messages_list})


@login_required
def message(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = staff
            msg.save()
            return redirect('staff_messages')
    else:
        form = MessageForm()

    return render(request, 'staff/send_message.html', {'form': form})


@login_required
def staff_leave_status(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    staff = get_object_or_404(Staff, id=user_id)
    leaves = LeaveApplication.objects.filter(staff=staff).order_by()
    return render(request, 'staff/leave_status.html', {'leaves': leaves})


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskUpdateForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully.")
            return redirect('staff_tasks')
    else:
        form = TaskUpdateForm(instance=task)
    return render(request, 'staff/update_task.html', {'form': form, 'task': task})


from django.http import JsonResponse
from django.utils import timezone
from django.contrib.auth import logout

@login_required
def check_tasks_and_logout(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Not logged in'})

    staff = get_object_or_404(Staff, id=user_id)
    today = timezone.now().date()

    # Check if any unsubmitted tasks exist for today
    pending_tasks = Task.objects.filter(staff=staff, due_date=today).exclude(status='Completed')

    if pending_tasks.exists():
        return JsonResponse({'success': False, 'message': 'Tasks pending'})

    # Update or create today's attendance record
    attendance, created = Attendance.objects.get_or_create(
        staff=staff,
        date=today,
        defaults={'status': 'Present'}
    )
    attendance.logout_time = timezone.now()
    attendance.save()

    logout(request)
    return JsonResponse({'success': True, 'message': 'Logout and attendance recorded'})

