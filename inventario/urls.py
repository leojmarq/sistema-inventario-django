from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='inventario/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.inicio, name='inicio'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('producto/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('producto/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('admin-panel/', views.panel_admin, name='panel_admin'),
    path('respaldar-bd/', views.respaldar_bd, name='respaldar_bd'),
    path('restaurar-bd/', views.restaurar_bd, name='restaurar_bd'),
    path('logs/', views.logs_sistema, name='logs_sistema'),
    path('reportes/', views.reportes, name='reportes'),
    path('reporte-inventario-pdf/', views.reporte_inventario_pdf, name='reporte_inventario_pdf'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('crear-categoria/', views.crear_categoria, name='crear_categoria'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuario/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('usuario/<int:user_id>/crear-perfil/', views.crear_perfil, name='crear_perfil'),
    path('perfil/<int:pk>/editar/', views.editar_perfil, name='editar_perfil'),
    path('producto/<int:pk>/movimiento/', views.registrar_movimiento, name='registrar_movimiento'),
]