# manager_app/forms.py
from django import forms
from .models import *

from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['staff', 'date', ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


from django import forms
from .models import PerformanceReview  # Assuming you have this model

from django import forms
from .models import PerformanceReview


class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = ['review_date', 'score', 'comments']  # Removed 'staff' from the form fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove 'staff' field handling here since we will assign it in the view


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'


# Staff/forms.py

from .models import LeaveApplication, Message
from django import forms


class StaffLeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }


from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message']  # Exclude sender as we will set it manually in the view

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        # Optionally, you can pre-select a receiver, if needed.
        # Example: self.fields['receiver'].initial = some_value


class ManagerProfileForm(forms.ModelForm):
    class Meta:
        model = Manager
        exclude = ['password', 'created_at']


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


from django import forms
from Staff.models import Task

from django.forms import DateInput, DateTimeInput


class TaskAssignForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'start_time', 'end_time']
        widgets = {
            'due_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'step': '1'  # allows seconds input
            }, format='%Y-%m-%dT%H:%M:%S'),
            'end_time': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'step': '1'
            }, format='%Y-%m-%dT%H:%M:%S'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['start_time', 'end_time']:
            if self.initial.get(field):
                self.initial[field] = self.initial[field].strftime('%Y-%m-%dT%H:%M:%S')


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'remarks', 'screenshot', 'submitted_at']
        widgets = {
            'submitted_at': forms.DateTimeInput(attrs={
                'type': 'datetime-local',  # enables date & time picker
                'class': 'form-control'
            }),
        }


from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'message']

    # Optionally, you can add custom validation for the fields here if needed
