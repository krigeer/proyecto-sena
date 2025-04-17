from django import forms
from inventario.models import centro,User, Rol, TypeDocument, Password, Ubication, Type_technologi, Markes, Place, Material_Didactico, Lend
from inventario import models
from django.core.validators import RegexValidator, EmailValidator


class RegistroUbicacion(forms.ModelForm):
    name_validator = RegexValidator(
        regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$',
        message="Solo se permiten letras y espacios."
    )

    id_centro = forms.ModelChoiceField(
        queryset =centro.objects.all(),
        label='Centro al que pertenece',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    name_Ubication = forms.CharField(
        max_length=100,
        label="Nombre de la Ubicación",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    description_ubication = forms.CharField(
    max_length=200,
    label="Descripción de la Ubicación",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = models.Ubication
        fields = ['id_centro','name_Ubication','description_ubication']


class RegistroTecnologico(forms.ModelForm):
    idType_technologi = forms.ModelChoiceField(
        queryset =models.Type_technologi.objects.all(),
        label='Tipo de Elemento',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
   
    caracteristics = forms.CharField(
    max_length=200,
    label="Caracteristicas",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    idMarke = forms.ModelChoiceField(
        queryset =models.Markes.objects.all(),
        label='Marca',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    series_Manufactures = forms.CharField(
    max_length=200,
    label="Serial Fabrica",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    series_sena = forms.CharField(
    max_length=200,
    label="Serial Sena",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    idUbication = forms.ModelChoiceField(
        queryset =models.Ubication.objects.all(),
        label='Ubicación',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    id_Place = forms.ModelChoiceField(
        queryset =models.Place.objects.all(),
        label='Estado',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model= models.Tecnology
        fields = ['idType_technologi','caracteristics','idMarke','series_Manufactures','series_sena','idUbication','id_Place']


class RegistroMateriales(forms.ModelForm):
    name_material = forms.CharField(
        label='Nombre del Material',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    

    description = forms.CharField(
    max_length=200,
    label="Descripción",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1})
    )

    quantity = forms.IntegerField(
        label='Cantidad',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    series_Manufactures = forms.CharField(
    max_length=200,
    label="Serial Fabrica",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1})
    )

    series_sena = forms.CharField(
    max_length=200,
    label="Serial SENA",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1})
    )

    id_Place=forms.ModelChoiceField(
        queryset = models.Place.objects.all(),
        label='Ubicación',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    

    class Meta:
        model = models.Material_Didactico
        fields =['name_material','description','quantity','series_Manufactures','series_sena','id_Place']


class Prestamo(forms.ModelForm):
    id_technologi = forms.ModelChoiceField(
        queryset =models.Tecnology.objects.all(),
        label='Elemento Tecnológico',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    id_user = forms.ModelChoiceField(
        queryset =User.objects.all(),
        label='Usuario',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    idMaterial_didactico = forms.ModelChoiceField(
        queryset =models.Material_Didactico.objects.all(),
        label='Material Didáctico',
        empty_label='Seleccione una opción',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    observation = forms.CharField(
    max_length=200,
    label="Descripción",
    widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 1})
    )
    class Meta:
        model = models.Lend
        fields = ['id_user','id_technologi','idMaterial_didactico','observation']


class ReporteForm(forms.ModelForm):
    class Meta:
        model = models.Report
        fields = '__all__'
        widgets = {
            }