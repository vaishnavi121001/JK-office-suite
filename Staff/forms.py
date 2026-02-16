from django import forms
from django.utils import timezone

from .models import Task, TaskSubmission


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['staff', 'title', 'description', 'status', 'due_date', 'start_time', 'end_time', 'remarks',
                  'screenshot']
        widgets = {
            'due_date': forms.TextInput(attrs={'type': 'date'}),  # Using TextInput with 'date' type
            'start_time': forms.TextInput(attrs={'type': 'datetime-local'}),  # Similarly for datetime-local
            'end_time': forms.TextInput(attrs={'type': 'datetime-local'}),  # Ensure correct HTML5 input types
        }


class TaskSubmissionForm(forms.ModelForm):
    status = forms.ChoiceField(choices=[('Completed', 'Completed'), ('Not Completed', 'Not Completed')])
    remarks = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter reason if not completed'}),
                              required=False)
    screenshot = forms.ImageField(required=False)

    class Meta:
        model = TaskSubmission
        fields = ['status', 'remarks', 'screenshot']

    def save(self, commit=True):
        task_submission = super().save(commit=False)
        task_submission.task.submitted_at = timezone.now()  # Set the current timestamp for submitted_at
        if commit:
            task_submission.save()
        return task_submission
