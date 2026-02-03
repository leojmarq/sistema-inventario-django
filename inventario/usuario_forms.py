from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['rol', 'departamento', 'telefono']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-select'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Ventas'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +1234567890'}),
        }