from django import forms
from . import models
from .models import User, Password
from django.utils import timezone
import hashlib

class Login(forms.Form):
    documento = forms.IntegerField(
        label='Documento', 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo'}))
    
    contrasena = forms.CharField(
        label='Contraseña', 
        max_length=100, 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña'}))


class ModificarUsuario(forms.Form):
    # Campos del modelo User
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    id_centro = forms.ModelChoiceField(
        queryset=User._meta.get_field('id_centro').remote_field.model.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Campo del modelo Password
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['email'].initial = self.user_instance.email
            self.fields['id_centro'].initial = self.user_instance.id_centro

            # Obtener contraseña más reciente
            try:
                password_obj = Password.objects.filter(id_user=self.user_instance).latest('creation_date')
                self.fields['password'].initial = password_obj.password
            except Password.DoesNotExist:
                pass
    def save(self):
        user = self.user_instance
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.id_centro = self.cleaned_data['id_centro']
        user.save()

        # Encriptar la contraseña con MD5
        raw_password = self.cleaned_data['password']
        hashed_password = hashlib.md5(raw_password.encode()).hexdigest()

        # Crear nuevo registro de contraseña
        Password.objects.create(
            id_user=user,
            password=hashed_password,
            creation_date=timezone.now().date(),
            expiration_date=timezone.now().date().replace(year=timezone.now().year + 1)
        )

        return user