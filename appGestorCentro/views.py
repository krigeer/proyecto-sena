from django.shortcuts import render, redirect, redirect, get_object_or_404
from inventario import models
from . import forms
# Create your views here.
def inicio(request):
    #valida que este logueado 
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')  # Por si falla
    usuario = request.session.get('NombreUsuario','NO')
    context = {
        'user': usuario,
        'id_user': id_usuario,
        }

    return render(request, 'gestorCentros.html', context)


def registerSede(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')
    if request.method == "POST":
        form = forms.NewSede(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appGestorCentro:gestorCentros')  
    else:
        form = forms.NewSede()
    return render(request, 'registerSedes.html', {'form': form, 'usuario': usuario})


def registerCentro(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')
    if request.method == "POST":
        form = forms.NewCentro(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appGestorCentro:gestorCentros') 
    else:
        form = forms.NewCentro()
    return render(request, 'registerCentros.html',{'form': form,})


def modifir(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')
    users = models.Sede.objects.select_related('id_City', 'id_City__id_department', 'id_City__id_Country')
    return render(request, 'configurations.html', {'users': users})


def infosede(request, id_sede):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')
    sede = get_object_or_404(models.Sede.objects.select_related(
        'id_City', 'id_City__id_department', 'id_City__id_Country'
    ), id_sede=id_sede)

    centros = models.centro.objects.filter(id_sede=sede)  # Obtener los centros de la sede

    return render(request, 'infoSede.html', {'sede': sede, 'centros': centros})