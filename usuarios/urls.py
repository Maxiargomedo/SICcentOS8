# filepath: c:\SIC final\compras_auth\usuarios\urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Vista para cerrar sesión
]