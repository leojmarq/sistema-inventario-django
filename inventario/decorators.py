from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def requiere_permiso(permiso):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                perfil = request.user.perfil
                if permiso == 'crear' and not perfil.puede_crear():
                    raise PermissionDenied("No tienes permisos para crear")
                elif permiso == 'editar' and not perfil.puede_editar():
                    raise PermissionDenied("No tienes permisos para editar")
                elif permiso == 'eliminar' and not perfil.puede_eliminar():
                    raise PermissionDenied("No tienes permisos para eliminar")
                elif permiso == 'reportes' and not perfil.puede_ver_reportes():
                    raise PermissionDenied("No tienes permisos para ver reportes")
            except:
                raise PermissionDenied("Usuario sin perfil asignado")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator