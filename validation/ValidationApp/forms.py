# ValidationApp/forms.py

from django import forms
from .models import Participant
from django.forms.widgets import SelectDateWidget
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate_number', 'model', 'make', 'color']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'date_of_birth', 'gender', 'phone', 'referanceNumber']
    date_of_birth = forms.DateField(widget=SelectDateWidget(years=range(1950, 2023)))