from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'rut', 'fecha_nacimiento', 'telefono', 'direccion', 'pertenece', 'role']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'rut', 'fecha_nacimiento', 'telefono', 'direccion', 'pertenece', 'role']