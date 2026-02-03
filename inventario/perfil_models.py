from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    ROLES = [
        ('admin', 'Administrador'),
        ('gerente', 'Gerente'),
        ('empleado', 'Empleado'),
        ('consulta', 'Solo Consulta'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES, default='empleado')
    departamento = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
    
    def puede_crear(self):
        return self.rol in ['admin', 'gerente', 'empleado']
    
    def puede_editar(self):
        return self.rol in ['admin', 'gerente', 'empleado']
    
    def puede_eliminar(self):
        return self.rol in ['admin', 'gerente']
    
    def puede_ver_reportes(self):
        return self.rol in ['admin', 'gerente']