from django.urls import path
from . import views


app_name = 'appIA'

urlpatterns = [
    path('', views.mensage, name='lora'),
    path('ia', views.mensage, name='send_message'),
    path('procesar_mensaje/', views.procesar_mensaje, name='procesar_mensaje'),
]