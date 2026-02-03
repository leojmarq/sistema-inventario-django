@login_required
def panel_admin(request):
    try:
        perfil = request.user.perfil
        if not perfil.puede_ver_reportes():
            messages.error(request, 'No tienes permisos para acceder al panel de administración')
            return redirect('inicio')
    except:
        messages.error(request, 'Usuario sin perfil asignado')
        return redirect('inicio')
    
    # Estadísticas básicas
    total_productos = Producto.objects.count()
    productos_stock_bajo = Producto.objects.filter(stock__lte=models.F('stock_minimo')).count()
    total_categorias = Categoria.objects.count()
    total_movimientos = MovimientoInventario.objects.count()
    
    # Productos con stock bajo
    productos_criticos = Producto.objects.filter(stock__lte=models.F('stock_minimo'))[:5]
    
    # Últimos movimientos
    ultimos_movimientos = MovimientoInventario.objects.select_related('producto').order_by('-fecha')[:10]
    
    context = {
        'perfil': perfil,
        'total_productos': total_productos,
        'productos_stock_bajo': productos_stock_bajo,
        'total_categorias': total_categorias,
        'total_movimientos': total_movimientos,
        'productos_criticos': productos_criticos,
        'ultimos_movimientos': ultimos_movimientos,
    }
    
    return render(request, 'inventario/panel_admin.html', context)