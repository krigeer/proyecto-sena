from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ingresar/', views.login, name='ingresar'),
    path('gestorCentro/', include('appGestorCentro.urls'), name='gestorCentro'),
    path('bodega/', include('appBodega.urls'), name='bodega'),
    path('Lora/', include('appIA.urls'), name='ia'),
    path('ajustes/<int:id>/', views.ajustes, name='ajustes'),
    path('actualizar_datos/<int:id>/', views.modificar_usuario, name='actualizar_datos'),
    path('salir', LogoutView.as_view(next_page='ingresar'), name='salir'),
]
