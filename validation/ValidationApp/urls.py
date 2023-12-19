# ValidationApp/urls.py

from django.urls import path
from .views import registration_view, registration_success_view, register_vehicle_view, login_view, home_view, logout_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', registration_view, name='register'),
    path('registration_success/', registration_success_view, name='registration_success'),
    path('register_vehicle/', register_vehicle_view, name='register_vehicle'),  # Update with actual view name
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', login_required(home_view), name='home')
    
]
