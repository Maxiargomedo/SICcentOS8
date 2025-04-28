from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('historial/', views.historial, name='historial'),
    path('revisor/', views.revisor, name='revisor'),
    path('aprobaciones/', views.aprobaciones, name='aprobaciones'),
    path('editar/<int:solicitud_id>/', views.editar_solicitud, name='editar_solicitud'),
    path('duplicar/<int:solicitud_id>/', views.duplicar_solicitud, name='duplicar_solicitud'),
    path('cambiar_estado/<int:solicitud_id>/', views.cambiar_estado, name='cambiar_estado'),
]