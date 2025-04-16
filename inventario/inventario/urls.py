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
    path('salir', LogoutView.as_view(next_page='ingresar'), name='salir'),
]
