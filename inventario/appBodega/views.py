from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from inventario.models import Tecnology, Material_Didactico
from inventario import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

def index(request):
    #valida que este logueado 
    usuario = request.session.get('NombreUsuario','NO')
    # inventarios = Inventario.objects.filter(sede=usuario.sede)
    # if not request.session.get('is_authenticated'):
    #     return redirect('/ingresar/') #redirige si no esta logeado
    return render(request, 'bodega.html', {'user': usuario})

def newTecnologi(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    user_id = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=user_id)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')  # Por si falla

    
    #formulario por metodo post
    if request.method == 'POST':
        form = forms.RegistroTecnologico(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Elemento Registrado')
            return redirect('bodega:bodega')
        else:
            print(f'error: {form.errors}')
    else:
        form = forms.RegistroTecnologico()
    #busqueda
    search_query = request.GET.get('search','')
    #filtro de busqueda
    equipos = models.Tecnology.objects.select_related('idType_technologi').all()
    if usuario.id_rol.name_rol == 'gestorCentros':  # Si tienes ese rol
        equipos = Tecnology.objects.select_related('idType_technologi').all()
    else:
        equipos = Tecnology.objects.select_related('idType_technologi').filter(idUbication__id_centro=usuario.id_centro)
    if search_query:
        equipos = equipos.filter(
            Q(id_Place__name_place__icontains=search_query) | #busca por estado ya sea prestado, en bodega, manteniemiento, etc
            Q(idUbication__name_Ubication__icontains=search_query) | #busca por ubicaciones, biblioteca, oficinas, ambientes
            Q(series_Manufactures__icontains=search_query) | # busca por serial de fabrica
            Q(series_sena__icontains=search_query) # busca por serial del sena
        )
    #paginacion
    paginator = Paginator(equipos, 30)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number) 
    return render(request, 'newTecnologia.html', {
        'form': form,
        'equipos': page_obj,  # Datos paginados
        'search_query': search_query  # Enviar búsqueda a la plantilla
    })


def newOtros(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    user_id = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=user_id)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')  # Por si falla
    #formulario registro materiales
    if request.method == 'POST':
        form = forms.RegistroMateriales(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Elemento Registrado')
            return redirect('bodega:bodega')
        else:
            print(form.errors)
    else:
        form =forms.RegistroMateriales()
    #obtiene la busqueda
    search_query = request.GET.get('search','')
     #filtro de busqueda
    materiales = models.Material_Didactico.objects.select_related('id_Place').all()
    if usuario.id_rol.name_rol == 'gestorCentros':  # Si tienes ese rol
        materiales = Material_Didactico.objects.select_related('id_Place').all()
    else:
        materiales = Material_Didactico.objects.select_related('id_Place').filter(idUbication__id_centro=usuario.id_centro)
    
    if search_query:
        materiales = materiales.filter(
            Q(series_Manufactures__icontains=search_query) |
            Q(series_sena__icontains=search_query) |
            Q(name_material__icontains=search_query)
        )
    #PAGINACION
    paginator = Paginator(materiales, 30)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'newOtros.html', {
        'form': form,
        'materiales': page_obj,  # Datos paginados
        'search_query': search_query  # Enviar búsqueda a la plantilla
    })

def newUbication(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    user_id = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=user_id)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')  # Por si falla
    # Manejo del formulario
    if request.method == 'POST':
        form = forms.RegistroUbicacion(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ubicación Registrada')
            return redirect('bodega:bodega')  # Se mantiene en la misma vista
        else:
            print(form.errors)
            messages.error(request, 'Ubicación no registrada')
    else:
        form = forms.RegistroUbicacion()

    # OBTENER EL TÉRMINO DE BÚSQUEDA
    search_query = request.GET.get('search', '')

    #FILTRAR UBICACIONES SI HAY BÚSQUEDA
    ubicaciones = models.Ubication.objects.select_related('id_centro').all()
    # if usuario.id_rol.name_rol == 'gestorCentros':  # Si tienes ese rol
    #     ubicaciones = Material_Didactico.objects.select_related('id_Place').all()
    # else:
    #     materiales = Material_Didactico.objects.select_related('id_Place').filter(idUbication__id_centro=usuario.id_centro)
    if search_query:
        ubicaciones = ubicaciones.filter(
            Q(name_Ubication__icontains=search_query) |  # Buscar por nombre de la ubicación
            Q(id_centro__name_centro__icontains=search_query)  # Buscar por nombre del centro
        )

    # PAGINACIÓN (30 ELEMENTOS POR PGINA)
    paginator = Paginator(ubicaciones, 30)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    return render(request, 'newUbication.html', {
        'form': form,
        'ubicaciones': page_obj,  # Datos paginados
        'search_query': search_query  # Enviar búsqueda a la plantilla
    })

def prestamo(request):
    if request.method == 'POST':
        form = forms.Prestamo(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prestamo Registrado')
            return redirect('bodega:bodega')
        else:
            print(form.errors)
            messages.error(request, 'Prestamo no registrado')
    else:
        form = forms.Prestamo()
    return render(request, 'prestamo.html',{'form': form})


def visualizar(request, id):
    context = {
        'centros': centro.objects.all(),  # Obtener todos los centros
        'ubicaciones': models.Ubication.objects.all(),  # Obtener todas las ubicaciones
        'tecnologias': get_object_or_404(models.Tecnology, idTecnology=id),  # Obtener todas las tecnologías
        'materiales': models.Material_Didactico.objects.all(),  # Obtener todos los materiales didácticos
    }
    return render(request, 'visualizar.html', context)

def visualizar(request, id):
    return render(request, 'detalles.html')