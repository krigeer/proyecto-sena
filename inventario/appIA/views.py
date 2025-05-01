from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
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
import random, re,os
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
import torch
from django.conf import settings
from inventario.models import Aprendizaje, Tag, Categoria, NivelDificultad, EjemploInteraccion
# Create your views here.
def mensage(request):
    if not request.session.get('is_authenticated'):
      return redirect('/ingresar/')  
    id_usuario = request.session.get('user_id')

    try:
        usuario = models.User.objects.get(id_user=id_usuario)
    except models.User.DoesNotExist:
        return redirect('/ingresar/')
    letra = usuario.first_name[0] if usuario.first_name else ""

    context = {
        'ia': 'L',
        'name_user': usuario,
        'usuario': letra,
    }

    return render(request, 'chat.html', context)

from django.http import JsonResponse
import json

class AsistenteIA:
    def __init__(self, modelo_path):
        self.modelo_path = modelo_path
        self.tokenizer = AutoTokenizer.from_pretrained(modelo_path)
        self.base_model = AutoModelForCausalLM.from_pretrained("datificate/gpt2-small-spanish")
        self.config = PeftConfig.from_pretrained(modelo_path)
        self.modelo = PeftModel.from_pretrained(self.base_model, modelo_path)
        self.modelo.eval()
        
        # Mover modelo a GPU 
        if torch.cuda.is_available():
            self.modelo.cuda()
    
    def _identificar_contexto(self, texto):
        """
        Identifica el contexto más probable basado en las palabras clave
        y el contenido del mensaje del usuario.
        """
        # Normalizar texto (lowercase, eliminar caracteres especiales)
        texto_norm = texto.lower()
        texto_norm = re.sub(r'[^\w\s]', '', texto_norm)
        palabras = texto_norm.split()
        
        # Buscar aprendizajes cuyas palabras clave aparezcan en el texto
        coincidencias = {}
        todos_aprendizajes = Aprendizaje.objects.filter(activo=True)
        
        # Si no hay aprendizajes, retornar None
        if not todos_aprendizajes.exists():
            return None, None
        
        for aprendizaje in todos_aprendizajes:
            if not aprendizaje.palabras_clave:
                continue
                
            # Contamos cuántas palabras clave coinciden
            coincidencia = 0
            for palabra_clave in aprendizaje.palabras_clave:
                if palabra_clave.lower() in texto_norm:
                    coincidencia += 1
            
            if coincidencia > 0:
                coincidencias[aprendizaje.id_aprendizaje] = coincidencia
        
        # Si no hay coincidencias, intentamos con categorías generales
        if not coincidencias:
            # Buscar aprendizajes con categoría "general"
            try:
                categoria_general = Categoria.objects.get(nombre="general")
                aprendizaje_general = Aprendizaje.objects.filter(categoria=categoria_general).first()
                if aprendizaje_general:
                    return aprendizaje_general, []
            except Categoria.DoesNotExist:
                pass
            
            # Si no hay categoría general, devolver el primer aprendizaje
            return todos_aprendizajes.first(), []
        
        # Obtener el aprendizaje con más coincidencias
        id_mejor_aprendizaje = max(coincidencias, key=coincidencias.get)
        mejor_aprendizaje = Aprendizaje.objects.get(id_aprendizaje=id_mejor_aprendizaje)
        
        # Buscar ejemplos relacionados
        ejemplos = EjemploInteraccion.objects.filter(aprendizaje=mejor_aprendizaje)
        
        return mejor_aprendizaje, ejemplos
    
    def _enriquecer_prompt(self, texto_usuario, aprendizaje, ejemplos):
        """
        Construye un prompt enriquecido con el contexto y ejemplos relevantes.
        """
        prompt_enriquecido = ""
        
        # Agregar contexto del aprendizaje
        if aprendizaje:
            prompt_enriquecido += f"### Contexto: {aprendizaje.contexto}\n\n"
            
            # Agregar un máximo de 2 ejemplos de interacción para no saturar el contexto
            if ejemplos:
                ejemplos_list = list(ejemplos)
                # Seleccionar 2 ejemplos aleatorios si hay más de 2
                if len(ejemplos_list) > 2:
                    ejemplos_list = random.sample(ejemplos_list, 2)
                    
                prompt_enriquecido += "### Ejemplos de interacción:\n"
                for ejemplo in ejemplos_list:
                    prompt_enriquecido += f"Usuario: {ejemplo.consulta_usuario}\n"
                    prompt_enriquecido += f"Respuesta: {ejemplo.respuesta_modelo}\n\n"
            
            # Si hay una respuesta esperada, la usamos como guía
            if aprendizaje.respuesta_esperada:
                prompt_enriquecido += f"### Patrón de respuesta: {aprendizaje.respuesta_esperada}\n\n"
        
        # Agregar la consulta del usuario
        prompt_enriquecido += f"### Pregunta: {texto_usuario.strip()}\n\n### Respuesta:"
        
        return prompt_enriquecido
    
    def generar_respuesta(self, texto_usuario):
        """
        Genera una respuesta basada en el texto del usuario y el contexto identificado.
        """
        # Identificar el contexto más relevante
        aprendizaje, ejemplos = self._identificar_contexto(texto_usuario)
        
        # Enriquecer el prompt con el contexto y ejemplos
        prompt_formateado = self._enriquecer_prompt(texto_usuario, aprendizaje, ejemplos)
        
        # Tokenizar 
        entrada = self.tokenizer(prompt_formateado, return_tensors="pt")
        
        # Mover a GPU si está disponible 
        if torch.cuda.is_available():
            entrada = {k: v.cuda() for k, v in entrada.items()}
        
        generacion_params = {
            "max_length": 256,
            "temperature": 0.5,           # Temperatura para creatividad
            "top_p": 0.92,                # Nucleus sampling
            "top_k": 50,                  # Top-k sampling
            "repetition_penalty": 1.5,    # Penalizar repeticiones
            "no_repeat_ngram_size": 3,    # Evitar repetir secuencias de 3+ tokens
            "do_sample": True,            # Usar sampling (no greedy)
            "pad_token_id": self.tokenizer.eos_token_id,
            "eos_token_id": self.tokenizer.eos_token_id,
            "num_return_sequences": 1     # Una respuesta
        }
        
        # Generar respuesta
        with torch.no_grad():  # No acumular gradientes durante la inferencia
            salida = self.modelo.generate(
                **entrada,
                **generacion_params
            )
        
        # Decodificar la respuesta
        respuesta_completa = self.tokenizer.decode(salida[0], skip_special_tokens=True)
        
        # Extraer solo la parte de respuesta
        if "### Respuesta:" in respuesta_completa:
            respuesta_final = respuesta_completa.split("### Respuesta:")[1].strip()
        else:
            respuesta_final = respuesta_completa.replace(prompt_formateado, "").strip()
        
        return respuesta_final


# Inicializar el asistente como variable global para reutilizarlo entre llamadas
asistente = None

def procesar_mensaje(request):
    global asistente
    
    modelo_path = "C:/Users/Alexander/OneDrive/Documentos/Crud inventario/proyecto-sena/inventario/appIA/modelo_ajustad"
    
    # Inicializar el asistente si no existe
    if asistente is None:
        asistente = AsistenteIA(modelo_path)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mensaje = data.get('mensaje', '')
            id_conversacion = data.get('id_conversacion', None)
            
            # Generar respuesta usando el asistente
            respuesta = asistente.generar_respuesta(mensaje)
            
            # Aquí podrías guardar el mensaje y la respuesta en la base de datos
            # para mantener un historial de conversaciones
            
            return JsonResponse({
                'status': 'success',
                'reply': respuesta,
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error al procesar mensaje: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


def buscar_aprendizaje(request):
    """
    Endpoint para buscar aprendizajes por palabras clave o categoría.
    Útil para la interfaz de administración.
    """
    if request.method == 'GET':
        query = request.GET.get('q', '')
        
        if not query:
            return JsonResponse({'status': 'error', 'message': 'Se requiere un término de búsqueda'}, status=400)
        
        # Buscar en palabras clave, prompt y categoría
        resultados = Aprendizaje.objects.filter(
            Q(prompt__icontains=query) | 
            Q(categoria__nombre__icontains=query) |
            Q(tags__nombre__icontains=query)
        ).distinct()
        
        # Formatear resultados
        data = [{
            'id': item.id_aprendizaje,
            'prompt': item.prompt[:100] + '...' if len(item.prompt) > 100 else item.prompt,
            'categoria': item.categoria.nombre,
            'tags': [tag.nombre for tag in item.tags.all()],
            'dificultad': item.dificultad.nombre
        } for item in resultados]
        
        return JsonResponse({
            'status': 'success',
            'count': len(data),
            'results': data
        })
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)