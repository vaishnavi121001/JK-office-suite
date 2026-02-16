from .models import RecruitmentPost
from django import forms
from django.utils import timezone
from .models import Salary, Staff, Manager


class RecruitmentPostForm(forms.ModelForm):
    class Meta:
        model = RecruitmentPost
        fields = '__all__'
        widgets = {
            'last_date': forms.DateInput(attrs={'type': 'date'}),
        }


class EmployeeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.full_name


class SalaryForm(forms.ModelForm):
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now
    )

    employee_type = forms.ChoiceField(choices=Salary.EMPLOYEE_TYPE_CHOICES)
    employee = EmployeeModelChoiceField(queryset=Staff.objects.none(), required=True)

    class Meta:
        model = Salary
        fields = [
            'employee_type', 'employee',
            'basic_salary', 'hra', 'ta',
            'bonus', 'deductions',
            'net_salary',  # Will be readonly
            'payment_date',
        ]
        widgets = {
            'net_salary': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(SalaryForm, self).__init__(*args, **kwargs)
        data = self.data or self.initial

        emp_type = data.get('employee_type')
        if emp_type == 'staff':
            self.fields['employee'].queryset = Staff.objects.all()
        elif emp_type == 'manager':
            self.fields['employee'].queryset = Manager.objects.all()

        self.fields['hra'].required = False
        self.fields['ta'].required = False
        self.fields['bonus'].required = False
        self.fields['deductions'].required = False

    def save(self, commit=True):
        instance = super().save(commit=False)
        employee = self.cleaned_data['employee']
        emp_type = self.cleaned_data['employee_type']

        if emp_type == 'staff':
            instance.staff = employee
            instance.manager = None
        elif emp_type == 'manager':
            instance.manager = employee
            instance.staff = None

        # Compute Net Salary
        basic = self.cleaned_data.get('basic_salary') or 0
        hra = self.cleaned_data.get('hra') or 0
        ta = self.cleaned_data.get('ta') or 0
        bonus = self.cleaned_data.get('bonus') or 0
        deductions = self.cleaned_data.get('deductions') or 0

        instance.net_salary = basic + hra + ta + bonus - deductions

        if commit:
            instance.save()
        return instance
