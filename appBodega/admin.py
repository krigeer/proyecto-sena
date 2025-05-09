from django.contrib import admin
from inventario import models
# Register your models here.
class TecnologyAdmin(admin.ModelAdmin):
    list_display = ('idTecnology', 'idType_technologi', 'idMarke', 'idUbication', 'id_Place')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(idUbication__id_centro=request.user.id_centro)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.idUbication.id_centro == request.user.id_centro
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.idUbication.id_centro == request.user.id_centro
        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.idUbication.id_centro = request.user.id_centro
        super().save_model(request, obj, form, change)

admin.site.register(models.Tecnology, TecnologyAdmin)


class MaterialDidacticoAdmin(admin.ModelAdmin):
    list_display = ('idMaterial_didactico', 'name_material', 'quantity', 'idUbication', 'id_Place')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(idUbication__id_centro=request.user.id_centro)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.idUbication.id_centro == request.user.id_centro
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return obj.idUbication.id_centro == request.user.id_centro
        return super().has_delete_permission(request, obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "idUbication" and not request.user.is_superuser:
            kwargs["queryset"] = models.Ubication.objects.filter(id_centro=request.user.id_centro)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.Material_Didactico, MaterialDidacticoAdmin)


class LendAdmin(admin.ModelAdmin):
    list_display = ('idLend', 'idTecnology', 'idMaterial_didactico', 'date_lend', 'date_return')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            models.Q(idTecnology__idUbication__id_centro=request.user.id_centro) |
            models.Q(idMaterial_didactico__idUbication__id_centro=request.user.id_centro)
        )

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            centro = request.user.id_centro
            return (
                (obj.idTecnology and obj.idTecnology.idUbication.id_centro == centro) or
                (obj.idMaterial_didactico and obj.idMaterial_didactico.idUbication.id_centro == centro)
            )
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

admin.site.register(models.Lend, LendAdmin)