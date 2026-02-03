from django import forms
from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Electrónicos'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción opcional'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if len(nombre) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
        
        # Verificar unicidad
        categorias_existentes = Categoria.objects.filter(nombre__iexact=nombre)
        if self.instance and self.instance.pk:
            categorias_existentes = categorias_existentes.exclude(pk=self.instance.pk)
        
        if categorias_existentes.exists():
            raise forms.ValidationError('Ya existe una categoría con este nombre')
        
        return nombre.title()