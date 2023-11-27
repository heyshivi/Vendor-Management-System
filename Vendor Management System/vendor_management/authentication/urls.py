# authentication/urls.py

from django.urls import path
from .views import Registration, Login

urlpatterns = [
    path('register/', Registration.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]
