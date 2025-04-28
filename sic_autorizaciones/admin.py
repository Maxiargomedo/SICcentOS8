from django.contrib import admin
from .models import SolicitudSIC

class SolicitudSICAdmin(admin.ModelAdmin):
    list_display = ('numero_sic', 'es_muestra', 'pertenece', 'solicitante', 'fecha_requerida', 'archivo')
    list_filter = ('es_muestra', 'pertenece', 'fecha_requerida')

admin.site.register(SolicitudSIC, SolicitudSICAdmin)