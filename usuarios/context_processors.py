def permisos_usuario(request):
    if request.user.is_authenticated:
        return {
            'is_admin': request.user.is_staff,
            'is_normal_user': request.user.role == 'usuario_normal',
            'is_revisor': request.user.role == 'revisor',
            'is_aprobador': request.user.role == 'aprobador',
        }
    return {}