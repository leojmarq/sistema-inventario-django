from django.contrib import admin
from django.contrib.auth.models import User
from .models import Categoria, Producto, MovimientoInventario, Perfil, LogSistema

@admin.register(LogSistema)
class LogSistemaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'accion', 'descripcion', 'fecha', 'ip_address']
    list_filter = ['accion', 'fecha']
    search_fields = ['usuario__username', 'descripcion']
    readonly_fields = ['usuario', 'accion', 'descripcion', 'fecha', 'ip_address']

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['user', 'rol', 'departamento']
    list_filter = ['rol']
    search_fields = ['user__username', 'user__email']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'categoria', 'precio', 'stock', 'necesita_restock']
    list_filter = ['categoria', 'fecha_creacion']
    search_fields = ['nombre', 'codigo']
    list_editable = ['precio', 'stock']

@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo', 'cantidad', 'motivo', 'fecha']
    list_filter = ['tipo', 'fecha']
    search_fields = ['producto__nombre', 'motivo']