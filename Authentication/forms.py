from .models import Manager
from .models import Staff

import re
from .models import Staff
from django import forms
from .models import Company


class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_email', 'company_phone', 'address']

    company_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}))
    company_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Email'}))
    company_phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Phone'}))
    address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Company Address', 'rows': 2}))

    def clean_company_name(self):
        name = self.cleaned_data.get('company_name')
        if not name:
            raise forms.ValidationError("Company name is required.")
        if len(name) < 3:
            raise forms.ValidationError("Company name must be at least 3 characters long.")
        return name

    def clean_company_email(self):
        email = self.cleaned_data.get('company_email')
        if not email:
            raise forms.ValidationError("Company email is required.")
        return email

    def clean_company_phone(self):
        phone = self.cleaned_data.get('company_phone')
        if not phone:
            raise forms.ValidationError("Company phone number is required.")
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            raise forms.ValidationError("Address is required.")
        if len(address) < 10:
            raise forms.ValidationError("Address must be at least 10 characters long.")
        return address


from django import forms
from .models import Director
from .validators import validate_company_code  # use the above function


class DirectorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = [
            'full_name', 'email', 'contact_number', 'adhar_card',
            'username', 'company_code', 'department', 'joining_date',
            'emergency_phone', 'address', 'qualifications', 'experience'
        ]
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'qualifications': forms.Textarea(attrs={'rows': 2}),
            'experience': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_contact_number(self):
        contact = self.cleaned_data['contact_number']
        if not contact.isdigit() or len(contact) != 10:
            raise forms.ValidationError("Enter a valid 10-digit contact number.")
        return contact

    def clean_emergency_phone(self):
        emergency = self.cleaned_data['emergency_phone']
        if not emergency.isdigit() or len(emergency) != 10:
            raise forms.ValidationError("Enter a valid 10-digit emergency phone number.")
        return emergency

    def clean_adhar_card(self):
        adhar = self.cleaned_data['adhar_card']
        if not adhar.isdigit() or len(adhar) != 12:
            raise forms.ValidationError("Enter a valid 12-digit Aadhaar number.")
        return adhar

    def clean_company_code(self):
        code = self.cleaned_data['company_code']
        validate_company_code(code)
        return code

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError("Username should not contain spaces.")
        return username


from .models import HR


class HRRegistrationForm(forms.ModelForm):
    class Meta:
        model = HR
        fields = [
            'full_name', 'email', 'contact_number', 'adhar_card',
            'username', 'company_code', 'department',
            'joining_date', 'emergency_phone',
            'address', 'qualifications', 'experience'
        ]
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_contact_number(self):
        contact = self.cleaned_data['contact_number']
        if not contact.isdigit() or len(contact) != 10:
            raise forms.ValidationError("Enter a valid 10-digit contact number.")
        return contact

    def clean_emergency_phone(self):
        emergency = self.cleaned_data['emergency_phone']
        if not emergency.isdigit() or len(emergency) != 10:
            raise forms.ValidationError("Enter a valid 10-digit emergency phone number.")
        return emergency

    def clean_adhar_card(self):
        adhar = self.cleaned_data['adhar_card']
        if not adhar.isdigit() or len(adhar) != 12:
            raise forms.ValidationError("Enter a valid 12-digit Aadhaar number.")
        return adhar

    def clean_company_code(self):
        code = self.cleaned_data['company_code']
        validate_company_code(code)
        return code

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError("Username should not contain spaces.")
        return username


from .models import Manager


class ManagerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = [
            'full_name', 'email', 'contact_number', 'adhar_card',
            'username', 'company_code', 'department',
            'joining_date', 'emergency_phone',
            'address', 'qualifications', 'experience'
        ]
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_contact_number(self):
        contact = self.cleaned_data['contact_number']
        if not contact.isdigit() or len(contact) != 10:
            raise forms.ValidationError("Enter a valid 10-digit contact number.")
        return contact

    def clean_emergency_phone(self):
        emergency = self.cleaned_data['emergency_phone']
        if not emergency.isdigit() or len(emergency) != 10:
            raise forms.ValidationError("Enter a valid 10-digit emergency phone number.")
        return emergency

    def clean_adhar_card(self):
        adhar = self.cleaned_data['adhar_card']
        if not adhar.isdigit() or len(adhar) != 12:
            raise forms.ValidationError("Enter a valid 12-digit Aadhaar number.")
        return adhar

    def clean_company_code(self):
        code = self.cleaned_data['company_code']
        validate_company_code(code)
        return code

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError("Username should not contain spaces.")
        return username

from django import forms
from .models import Staff
from .models import Company
from django.core.exceptions import ValidationError
import re


class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model = Staff
        exclude = ['manager', 'salary', 'password', 'qr_code','user']  # password is auto-generated
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_company_code(self):
        code = self.cleaned_data.get('company_code')
        if not Company.objects.filter(company_code=code).exists():
            raise ValidationError("Invalid company code.")
        return code

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Staff.objects.filter(username=username).exists():
            raise ValidationError("Username already exists. Please choose a different one.")
        return username

    def clean_adhar_card(self):
        adhar = self.cleaned_data.get('adhar_card')
        if not re.match(r'^\d{12}$', adhar):
            raise ValidationError("Aadhar card number must be exactly 12 digits.")
        return adhar

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Staff.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def clean_contact_number(self):
        contact = self.cleaned_data.get('contact_number')
        if not re.match(r'^\d{10}$', contact):
            raise ValidationError("Contact number must be exactly 10 digits.")
        return contact



class ManagerLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
