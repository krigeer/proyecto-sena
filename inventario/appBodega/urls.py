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
    path('detalles/<int:id>/',views.visualizar, name='detalles')
    ]