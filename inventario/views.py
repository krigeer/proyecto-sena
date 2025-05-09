from django.shortcuts import render,redirect, get_object_or_404
from . import forms, models
from django.contrib.auth import login  as auth_login
from django.contrib.auth.models import User
import re
import hashlib
from django.contrib import messages
def index(request):
    return render(request, 'index.html')

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as DjangoUser  # Si tienes el modelo de usuario original
import hashlib
from django.contrib import messages
from django.shortcuts import render, redirect

def login(request):
    if request.method == 'POST':
        form = forms.Login(request.POST)
        if form.is_valid():
            documento = form.cleaned_data['documento']
            contrasena = form.cleaned_data['contrasena']

            if not documento or not contrasena:
                messages.error(request, 'Los campos no pueden estar vacíos')
                return render(request, "ingresar.html", {'form': form})

            try:
                usuario = models.User.objects.get(document=documento)

                password_enviado_hash = hashlib.md5(contrasena.encode()).hexdigest()
                password_guardado = models.Password.objects.get(id_user=usuario.id_user)

                if password_guardado.password != password_enviado_hash:
                    messages.error(request, 'Contraseña incorrecta')
                    return render(request, "ingresar.html", {'form': form})

                # GUARDAR INFO EN SESIÓN
                request.session['user_id'] = usuario.id_user
                request.session['NombreUsuario'] = usuario.first_name
                request.session['id_centro'] = usuario.id_centro_id
                request.session['is_authenticated'] = True

                # Redirección por rol
                if usuario.id_rol:
                    rol = usuario.id_rol.name_rol
                    if rol == 'instructor':
                        return redirect('appInstructor:instructor')
                    elif rol == 'bodega':
                        return redirect('appBodega:bodega')
                    elif rol == 'mesaAyuda':
                        return redirect('appMesaAyuda:mesaAyuda')
                    elif rol == 'gestorCentros':
                        return redirect('appGestorCentro:gestorCentros')
                    else:
                        messages.error(request, 'Rol no reconocido')

            except models.User.DoesNotExist:
                messages.error(request, 'No existe un usuario con ese documento')
            except models.Password.DoesNotExist:
                messages.error(request, 'No se encontró la contraseña para el usuario')

    else:
        form = forms.Login()

    return render(request, 'ingresar.html', {'form': form})


def ajustes(request, id):
    if not request.session.get('is_authenticated'):
        return redirect('/ingresar/')  # Redirige si no está logueado

    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')  # Por si falla
    context ={'usuario': usuario,}
    return render(request, 'users.html',context)

