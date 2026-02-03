@login_required
def crear_perfil(request):
    from .models import Perfil
    
    # Crear perfil automáticamente si no existe
    perfil, created = Perfil.objects.get_or_create(
        user=request.user,
        defaults={'rol': 'admin'}  # Por defecto admin para el primer usuario
    )
    
    if created:
        messages.success(request, f'Perfil creado como {perfil.get_rol_display()}')
    
    return redirect('panel_admin')