from django.shortcuts import render, redirect
from django.urls import path
from . import views

app_name = 'appBodega'

urlpatterns =[
    path('', views.index, name='bodega'),
    path('newTecnologi/', views.newTecnologi, name='newTecnologi'),
    path('newOtros/', views.newOtros, name='newOtros'),
    path('newUbication/',views.newUbication, name='newUbication'),
    path('prestamo/', views.prestamo, name='prestamo'),
    path('mesaAyuda/', views.mesaAyuda, name='mesaAyuda'),
    path('newReport/', views.newReporte, name='newReport'),
    path('detalle/<int:id>/', views.visualizar, name='detalles'),
    path('deatelleOtros/<int:id>/', views.visualizarMaterial, name='detalleOtros'),
    path('detalle_reporte/<int:id>/',views.visualizar, name='detalle_reporte'),
    path('actualiar-equipo/<int:id>/', views.actualizarTecnologia, name='actualizar-equipo'),
    path('actualizar-otros/<int:id>/', views.actualizarMaterial, name='actualizar-otros'),
    ]