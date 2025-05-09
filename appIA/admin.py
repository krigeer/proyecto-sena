from django.contrib import admin
from inventario import  models
# Register your models here.

admin.site.register(models.Tag)
admin.site.register(models.Categoria)
admin.site.register(models.NivelDificultad)
admin.site.register(models.Aprendizaje)
