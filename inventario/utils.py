from .models import LogSistema

def registrar_log(usuario, accion, descripcion, request=None):
    """Registra una acción en el log del sistema"""
    ip_address = None
    if request:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    
    LogSistema.objects.create(
        usuario=usuario,
        accion=accion,
        descripcion=descripcion,
        ip_address=ip_address
    )