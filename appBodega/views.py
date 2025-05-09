from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from inventario.models import Tecnology, Material_Didactico
from inventario import models
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base64
import io

def index(request):
    #valida que este logueado 
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')  # Por si falla
    usuario = request.session.get('NombreUsuario','NO')
    
    context = {
        'user': usuario,
        'app': 'appBodega',
        'id_user': id_usuario,
        }
    return render(request, 'bodega.html', context) 

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
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')
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
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')
    context = {
        'centros': models.centro.objects.all(),  # Obtener todos los centros
    }
    return render(request, 'visualizar.html', context)

def mesaAyuda(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')
    
    # OBTENER EL TÉRMINO DE BÚSQUEDA
    search_query = request.GET.get('search', '')

    #FILTRAR UBICACIONES SI HAY BÚSQUEDA
    ubicaciones = models.Report.objects.all()
    # if usuario.id_rol.name_rol == 'gestorCentros':  # Si tienes ese rol
    #     ubicaciones = Material_Didactico.objects.select_related('id_Place').all()
    # else:
    #     materiales = Material_Didactico.objects.select_related('id_Place').filter(idUbication__id_centro=usuario.id_centro)
    if search_query:
        ubicaciones = ubicaciones.filter(
            Q(id_user__first_name__icontains=search_query) |  
            Q(id_centro__name_centro__icontains=search_query) | 
            Q(id_user__document__icontains=search_query)
        )

    # PAGINACIÓN (30 ELEMENTOS POR PGINA)
    paginator = Paginator(ubicaciones, 30)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    # Obtener reportes
    reportes = models.Report.objects.select_related('id_user').all().values(
        'id_user__first_name', 'id_user__last_name'
    )
    df = pd.DataFrame(reportes)
    df["nombre_completo"] = df["id_user__first_name"]
    conteo = df["nombre_completo"].value_counts()

    # Gráfico de barras (usuarios)
    # grafico_1 = generar_grafico_barras(conteo, 'Usuarios con más reportes', 'Cantidad de reportes')

    # # Gráfico de torta (tecnología con más reportes)
    # reportes_tec = models.Report.objects.filter(idTecnology__isnull=False).select_related('idTecnology').values('idTecnology__idTecnology')
    # df_tec = pd.DataFrame(reportes_tec)
    # conteo_tec = df_tec['idTecnology__idTecnology'].value_counts()
    # grafico_2 = generar_grafico_torta(conteo_tec, 'Tecnología más reportada')

    # # Gráfico de torta (material didáctico con más reportes)
    # reportes_mat = models.Report.objects.filter(idMaterial_didactico__isnull=False).select_related('idMaterial_didactico').values('idMaterial_didactico__idMaterial_didactico')
    # df_mat = pd.DataFrame(reportes_mat)
    # conteo_mat = df_mat['idMaterial_didactico__idMaterial_didactico'].value_counts()
    # grafico_3 = generar_grafico_torta(conteo_mat, 'Material didáctico más reportado')

    rereportes = models.Report.objects.all()
    context = {
        'usuario': usuario,
        # 'grafico_1': grafico_1,
        # 'grafico_2': grafico_2,
        # 'grafico_3': grafico_3,
        'reportes': rereportes,
        'ubicaciones': page_obj,  
        'search_query': search_query   
    }

    return render(request, 'mesaAyuda.html', context)


def generar_grafico_barras(conteo, titulo, ylabel):
    if conteo.empty:
        return ""
    plt.figure(figsize=(8, 5))
    conteo.plot(kind='bar', color='steelblue')
    plt.title(titulo)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return img


def generar_grafico_torta(conteo, titulo):
    if conteo.empty:
        return ""
    plt.figure(figsize=(6, 6))
    conteo.plot(kind='pie', autopct='%1.1f%%', startangle=90)
    plt.title(titulo)
    plt.ylabel('')
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return img

def newReporte(request):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')  # Por si falla
    usuario = request.session.get('NombreUsuario','NO')
    if request.method == 'POST':
        form = forms.ReporteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reporte creado exitosamente')
            return redirect('index')
    else:
        form = forms.ReporteForm()
    return render(request, 'newReport.html',  {'form': form, 'id_user': id_usuario})

