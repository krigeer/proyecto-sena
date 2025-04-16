from django import forms
from inventario  import models
from django.core.validators import RegexValidator, EmailValidator

class NewSede(forms.ModelForm):
    name_validator = RegexValidator(
        regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
        message="Solo se permiten letras y espacios."
    )

    id_City = forms.ModelChoiceField(
        queryset=models.City.objects.all(),
        label='Ciudad de la Sede',
        empty_label="Seleccione una opción",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    name_sede = forms.CharField(
        max_length=100,
        label="Nombre de la sede",
        validators=[name_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    direccion_sede = forms.CharField(
        max_length=100,
        label="Dirección de la sede",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    contact_one = forms.IntegerField(
        required=True,
        label="Contacto de la sede",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    encargate_register = forms.ModelChoiceField(
        queryset=models.User.objects.all(),
        label='Encargado del Registro',
        empty_label="Seleccione una opción",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = models.Sede
        fields = ['id_City', 'name_sede', 'direccion_sede', 'contact_one',  'encargate_register']


class NewCentro(forms.ModelForm):
    name_validator = RegexValidator(
     regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
     message="Solo se permiten letras y espacios."
    )  
    id_sede = forms.ModelChoiceField(
        queryset=models.Sede.objects.all(),
        label='Sede en la que esta el centro',
        empty_label="Seleccione una opción",
         widget=forms.Select(attrs={'class': 'form-select'})
    )
    name_centro = forms.CharField(
        max_length=100,
        label='Nombre del Centro',
        validators=[name_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    encargado_registro = forms.ModelChoiceField(
        queryset=models.User.objects.all(),
        label='Encargado del Registro',
        empty_label="Seleccione una opción",
        widget=forms.Select(attrs={'class': 'form-select'})
    )


    class Meta:
        model = models.centro
        fields = ['id_sede','name_centro','descripcion_centro','encargado_registro']

         
  
  
  