from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SolicitudSICForm
from sic_autorizaciones.models import SolicitudSIC
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import SolicitudSICForm
from .models import SolicitudSIC
from django.shortcuts import get_object_or_404

def is_revisor(user):
    return user.role == 'revisor' or user.is_staff

def is_aprobador(user):
    return user.role == 'aprobador' or user.is_staff

@login_required
@user_passes_test(is_revisor)
def revisor(request):
    return render(request, 'revisor.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'login.html')

@login_required
def historial(request):
    solicitudes = SolicitudSIC.objects.filter(solicitante=request.user)
    for solicitud in solicitudes:
        print(solicitud.numero_sic)  # Depuración: Verifica que cada solicitud tenga un número SIC
    return render(request, 'historial.html', {'solicitudes': solicitudes})


@login_required
def home(request):
    if request.method == 'POST':
        form = SolicitudSICForm(request.POST, request.FILES, user=request.user)  # Incluye request.FILES
        if form.is_valid():
            solicitud = form.save(commit=False)
            otro_solicitante = request.POST.get('otro_solicitante', '').strip()
            if otro_solicitante:
                solicitud.otro_solicitante = f"{request.user.username} ({otro_solicitante})"
            else:
                solicitud.otro_solicitante = request.user.username
            solicitud.solicitante = request.user
            solicitud.save()
            return redirect('historial')
    else:
        form = SolicitudSICForm(user=request.user)

    ultimo_sic = SolicitudSIC.objects.last()
    numero_sic = ultimo_sic.numero_sic + 1 if ultimo_sic else 1

    return render(request, 'home.html', {
        'form': form,
        'numero_sic': numero_sic,
        'solicitante': request.user.username,
    })
@login_required
def editar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSIC, numero_sic=solicitud_id, solicitante=request.user, estado="Rechazado")
    if request.method == 'POST':
        form = SolicitudSICForm(request.POST, request.FILES, instance=solicitud, user=request.user)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.estado = "Pendiente"  # Cambia el estado a pendiente
            solicitud.editada = True  # Marca la solicitud como editada
            solicitud.save()
            return redirect('historial')
    else:
        form = SolicitudSICForm(instance=solicitud, user=request.user)
    return render(request, 'editar_solicitud.html', {'form': form})

@login_required
def duplicar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSIC, numero_sic=solicitud_id, solicitante=request.user)
    if request.method == 'POST':
        form = SolicitudSICForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            nueva_solicitud = form.save(commit=False)
            nueva_solicitud.solicitante = request.user  # Asigna el usuario autenticado
            nueva_solicitud.estado = "Pendiente"  # La nueva solicitud siempre estará pendiente
            nueva_solicitud.save()
            return redirect('historial')
    else:
        form = SolicitudSICForm(initial={
            'es_muestra': solicitud.es_muestra,
            'pertenece': solicitud.pertenece,
            'fecha_requerida': solicitud.fecha_requerida,
            'descripcion': solicitud.descripcion,
            'especificacion_tecnica': solicitud.especificacion_tecnica,
            'cantidad': solicitud.cantidad,
            'unidad': solicitud.unidad,
            'comentario': solicitud.comentario,
        }, user=request.user)
    return render(request, 'duplicar_solicitud.html', {'form': form})

@login_required
@user_passes_test(is_revisor)
def cambiar_estado(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudSIC, numero_sic=solicitud_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['Pendiente', 'Autorizado', 'Rechazado']:
            solicitud.estado = nuevo_estado
            solicitud.save()
            messages.success(request, f"El estado de la solicitud {solicitud.numero_sic} ha sido actualizado a {nuevo_estado}.")
        else:
            messages.error(request, "Estado inválido.")
        return redirect('historial')
    return render(request, 'cambiar_estado.html', {'solicitud': solicitud})

@login_required
def aprobaciones(request):
    solicitudes_pendientes = SolicitudSIC.objects.filter(estado="Pendiente")
    solicitudes_aprobadas = SolicitudSIC.objects.filter(estado="Autorizado")

    if request.method == 'POST':
        solicitud_numero_sic = request.POST.get('solicitud_numero_sic')  # Cambiar a numero_sic
        accion = request.POST.get('accion')
        solicitud = get_object_or_404(SolicitudSIC, numero_sic=solicitud_numero_sic)  # Usar numero_sic

        if accion == 'aprobar':
            solicitud.estado = "Autorizado"
            solicitud.save()
            messages.success(request, f"La solicitud {solicitud.numero_sic} ha sido aprobada.")
        elif accion == 'rechazar':
            solicitud.estado = "Rechazado"
            solicitud.save()
            messages.error(request, f"La solicitud {solicitud.numero_sic} ha sido rechazada.")
        return redirect('aprobaciones')

    return render(request, 'aprobaciones.html', {
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aprobadas': solicitudes_aprobadas,
    })

