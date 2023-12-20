# ValidationApp/models.py

from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import date

def validate_email_domain(value):
    if not value.endswith('ur.ac.rw'):
        raise ValidationError(_('Email must end with ".ur.ac.rw"'))
    if '@' not in value:
        raise ValidationError(_('Email must contain @ character'))
    if Participant.objects.filter(email__iexact=value).exists():
        raise ValidationError(_('This email address is already registered. Please use a different one.'))

def validate_phone_number(value):
    if not value.startswith('+250'):
        raise ValidationError(_('Phone number should start with +250'))
    

def validate_reference_number(value):
    if not 99 <= value <= 999:
        raise ValidationError(_('Reference number should be between 99 and 999'))

def validate_age(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if age < 18:
        raise ValidationError(_('Age must be 18 or older'))

def validate_gender(value):
    if value not in ['M', 'F', 'O']:
        raise ValidationError(_('Gender must be "M", "F", or "O"'))

def validate_plate_number(value):
    plate_number_regex = r'^(RA[ABCDEFGH]|RNP|RDF|GR|IT)\d{3}[A-Za-z]$'
    validator = RegexValidator(regex=plate_number_regex, message='Invalid plate number format.')
    validator(value)

class Participant(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(validators=[validate_email_domain])
    date_of_birth = models.DateField(validators=[validate_age])
    gender = models.CharField(max_length=1, validators=[validate_gender])
    phone = models.CharField(max_length=15, validators=[validate_phone_number])
    referanceNumber = models.PositiveIntegerField(validators=[validate_reference_number])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Vehicle(models.Model):
    plate_number = models.CharField(max_length=15, validators=[validate_plate_number])
    model = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.make} {self.model}"
