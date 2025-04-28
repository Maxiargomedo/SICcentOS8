import os
from datetime import datetime
from django.db import models
from django.conf import settings

def upload_to(instance, filename):
    # Generar carpeta con formato día_mes_año
    today = datetime.now().strftime('%d_%m_%Y')
    return os.path.join(f'archivos/{today}', filename)

class SolicitudSIC(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Autorizado', 'Autorizado'),
        ('Rechazado', 'Rechazado'),
    ]

    numero_sic = models.AutoField(primary_key=True)
    es_muestra = models.BooleanField(default=False)
    pertenece = models.CharField(max_length=255, default="Sección desconocida")
    fecha_sic = models.DateField(auto_now_add=True)
    fecha_requerida = models.DateField(null=True, blank=True)
    solicitante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='solicitudes',
        null=False  # Asegúrate de que no permita valores nulos
    )
    otro_solicitante = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField()
    especificacion_tecnica = models.TextField(null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    unidad = models.CharField(max_length=50)
    comentario = models.TextField(null=True, blank=True)
    archivo = models.FileField(upload_to='uploads/', null=True, blank=True)  # Configuración para guardar archivos
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    editada = models.BooleanField(default=False)  # Campo para rastrear si fue editada

    def __str__(self):
        return f"SIC {self.numero_sic} - {self.solicitante.username}"
    
class Meta:
    permissions = [
        ("can_review", "Puede revisar solicitudes"),
        ("can_approve", "Puede aprobar solicitudes"),
    ]
