from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    pertenece = models.CharField(max_length=255, null=True, blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    ROLE_CHOICES = [
        ('administrador', 'Administrador'),
        ('usuario_normal', 'Usuario Normal'),
        ('revisor', 'Usuario Revisor'),
        ('aprobador', 'Usuario Ve Solicitudes Aprobadas'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario_normal')

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    