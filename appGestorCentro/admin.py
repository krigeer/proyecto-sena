from django.contrib import admin
from inventario import models
# Register your models here.
admin.site.register(models.Country)
admin.site.register(models.Department)
admin.site.register(models.City)
admin.site.register(models.Sede)
admin.site.register(models.centro)
admin.site.register(models.Rol)
admin.site.register(models.TypeDocument)
admin.site.register(models.Statu)
admin.site.register(models.User)
admin.site.register(models.Password)


admin.site.register(models.Ubication)
admin.site.register(models.Status_inventari)
admin.site.register(models.Place)
admin.site.register(models.Type_technologi)
admin.site.register(models.Markes)


admin.site.register(models.Type_report)
admin.site.register(models.Status_report)
admin.site.register(models.Priority_report)
admin.site.register(models.Report)



