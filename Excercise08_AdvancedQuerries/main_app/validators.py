from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re


def validate_name(name):
    if not re.fullmatch(r'[A-Za-z ]+', name):
        raise ValidationError('Name can only contain letters and spaces')


# def validate_name(value):
#     for char in value:
#         if not char.isalpha() or char.isspace():
#             raise ValidationError('Name can only contain letters and spaces')


def phone_validator(phone_number):
    if not re.fullmatch(r'^\+359\d{9}$', phone_number):
        raise ValidationError(f"Phone number must start with '+359' followed by 9 digits")


