from django import forms
from .models import SolicitudSIC

class SolicitudSICForm(forms.ModelForm):
    class Meta:
        model = SolicitudSIC
        fields = [
            'es_muestra', 'pertenece', 'fecha_requerida', 'otro_solicitante',
            'descripcion', 'especificacion_tecnica', 'cantidad',
            'unidad', 'comentario', 'archivo'
        ]
        widgets = {
            'es_muestra': forms.Select(choices=[(False, 'No'), (True, 'Sí')]),
            'fecha_requerida': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'especificacion_tecnica': forms.Textarea(attrs={'rows': 3}),
            'comentario': forms.Textarea(attrs={'rows': 2}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtén el usuario autenticado
        super().__init__(*args, **kwargs)
        if user:
            # Configura el valor inicial de "Pertenece a"
            self.fields['pertenece'].initial = user.pertenece
            # Configura el valor inicial de "Otro solicitante"
            self.fields['otro_solicitante'].initial = user.get_full_name()