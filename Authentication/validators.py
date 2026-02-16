from .models import Company
from django.core.exceptions import ValidationError


def validate_company_code(code):
    if not Company.objects.filter(company_code=code).exists():
        raise ValidationError("Invalid company code. Please enter a valid code.")
