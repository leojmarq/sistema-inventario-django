from django import forms
from .models import Producto, Categoria, MovimientoInventario
import re

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo', 'categoria', 'precio', 'stock', 'stock_minimo', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Laptop Dell'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: PROD001'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', nombre):
            raise forms.ValidationError('El nombre solo puede contener letras, números, espacios y guiones')
        return nombre.title()

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if len(codigo) < 3:
            raise forms.ValidationError('El código debe tener al menos 3 caracteres')
        if not re.match(r'^[A-Z0-9\-_]+$', codigo.upper()):
            raise forms.ValidationError('El código solo puede contener letras mayúsculas, números y guiones')
        
        codigo_upper = codigo.upper()
        
        # Verificar unicidad - excluir el producto actual si estamos editando
        productos_existentes = Producto.objects.filter(codigo=codigo_upper)
        if self.instance and self.instance.pk:
            productos_existentes = productos_existentes.exclude(pk=self.instance.pk)
        
        if productos_existentes.exists():
            raise forms.ValidationError('Ya existe un producto con este código')
        
        return codigo_upper

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0')
        if precio > 999999.99:
            raise forms.ValidationError('El precio no puede ser mayor a $999,999.99')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo')
        if stock > 999999:
            raise forms.ValidationError('El stock no puede ser mayor a 999,999')
        return stock

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo is None:
            raise forms.ValidationError('Este campo es requerido')
        if stock_minimo < 1:
            raise forms.ValidationError('El stock mínimo debe ser al menos 1')
        if stock_minimo > 9999:
            raise forms.ValidationError('El stock mínimo no puede ser mayor a 9,999')
        return stock_minimo
    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get('stock')
        stock_minimo = cleaned_data.get('stock_minimo')
        
        # Solo validar si ambos campos tienen valores válidos
        if stock is not None and stock_minimo is not None and stock >= 0 and stock_minimo >= 0:
            if stock > 0 and stock_minimo > stock:
                self.add_error('stock_minimo', 'El stock mínimo no puede ser mayor al stock actual')
        
        return cleaned_data

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['tipo', 'cantidad', 'motivo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo del movimiento'}),
        }

    def __init__(self, *args, **kwargs):
        self.producto = kwargs.pop('producto', None)
        super().__init__(*args, **kwargs)

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        if cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0')
        if cantidad > 99999:
            raise forms.ValidationError('La cantidad no puede ser mayor a 99,999')
        
        # Validar stock suficiente para salidas
        if self.cleaned_data.get('tipo') == 'salida' and self.producto:
            if cantidad > self.producto.stock:
                raise forms.ValidationError(f'Stock insuficiente. Disponible: {self.producto.stock}')
        
        return cantidad

    def clean_motivo(self):
        motivo = self.cleaned_data['motivo']
        if len(motivo) < 5:
            raise forms.ValidationError('El motivo debe tener al menos 5 caracteres')
        if len(motivo) > 200:
            raise forms.ValidationError('El motivo no puede tener más de 200 caracteres')
        return motivo.strip()