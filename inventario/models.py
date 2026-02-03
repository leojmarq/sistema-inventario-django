from django.db import models
from django.contrib.auth.models import User

class LogSistema(models.Model):
    ACCIONES = [
        ('crear', 'Crear'),
        ('editar', 'Editar'),
        ('eliminar', 'Eliminar'),
        ('login', 'Iniciar Sesión'),
        ('logout', 'Cerrar Sesión'),
        ('respaldo', 'Respaldo BD'),
        ('restaurar', 'Restaurar BD'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.usuario.username} - {self.get_accion_display()} - {self.fecha}"
    
    class Meta:
        ordering = ['-fecha']

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

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def necesita_restock(self):
        return self.stock <= self.stock_minimo

class MovimientoInventario(models.Model):
    TIPOS = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPOS)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad}"