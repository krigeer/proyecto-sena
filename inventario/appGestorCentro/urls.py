from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'appGestorCentro'
urlpatterns = [
    path('', views.inicio, name='gestorCentros'),
    path('registroSedes/', views.registerSede, name='registroSedes'),
    path('Centros/', views.registerCentro, name='Centros'),
    path('sedes/', views.modifir, name='sedes'),
    path('infoSede/<int:id_sede>/', views.infosede, name='infoSede')

]
