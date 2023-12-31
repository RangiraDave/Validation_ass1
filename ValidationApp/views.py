# ValidationApp/views.py

from django.shortcuts import render, redirect
from .forms import RegistrationForm, VehicleForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.forms import formset_factory
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler for application logs
handler = logging.FileHandler('logs/application.log')
handler.setLevel(logging.INFO)

# Formatter for application logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

easyaudit_logger = logging.getLogger('easyaudit')
easyaudit_logger.setLevel(logging.DEBUG)

easyaudit_handler = logging.FileHandler('logs/easyaudit.log')
easyaudit_handler.setLevel(logging.DEBUG)

easyaudit_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
easyaudit_handler.setFormatter(easyaudit_formatter)

easyaudit_logger.addHandler(easyaudit_handler)

def registration_view(request):
    VehicleFormSet = formset_factory(VehicleForm, extra=1)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        formset = VehicleFormSet(request.POST, prefix='vehicle')

        if form.is_valid() and formset.is_valid():
            participant = form.save()
            for vehicle_form in formset:
                if vehicle_form.cleaned_data:
                    vehicle = vehicle_form.save(commit=False)
                    vehicle.participant = participant
                    vehicle.save()

            return redirect('registration_success')
        else:
            print(formset.errors)
    else:
        form = RegistrationForm()
        formset = VehicleFormSet(prefix='vehicle')

    return render(request, 'registration.html', {'form': form, 'formset': formset})

def registration_success_view(request):
    return render(request, 'registration_success.html')

@csrf_protect
def register_vehicle_view(request):
    VehicleFormSet = formset_factory(VehicleForm, extra=1)  # Set extra to the number of forms you want initially

    if request.method == 'POST':
        formset = VehicleFormSet(request.POST, prefix='vehicles')
        if formset.is_valid():
            for form in formset:
                if form.has_changed():
                    form.save()
            return redirect('registration_success')
        else:
            print(formset.errors)
    else:
        formset = VehicleFormSet(prefix='vehicles')

    return render(request, 'register_vehicle.html', {'formset': formset})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    return render(request, 'home.html')
