from django import forms
from . import models
class Login(forms.Form):
    documento = forms.IntegerField(
        label='Documento', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo'}))
    
    contrasena = forms.CharField(
        label='Contraseña', 
        max_length=100, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}))


