from django.shortcuts import render, redirect
from usuarios.models import CustomUser
from django.contrib.auth.decorators import login_required
from sic_autorizaciones.forms import SolicitudSICForm
from sic_autorizaciones.models import SolicitudSIC
# filepath: c:\SIC final\compras_auth\usuarios\views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige al home después de iniciar sesión
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirigir al login después de cerrar sesión