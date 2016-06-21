# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Mascota, Vacuna, Desparacitante, EstadoMascota

class VacunaInline(admin.TabularInline):
    model = Vacuna
    fieldsets = [
        ('Vacunas', {'fields': ['vacuna','fecha']}),
    ]
    extra = 1

class DesparacitanteInline(admin.TabularInline):
    model = Desparacitante
    fieldsets = [
        ('Desparacitantes', {'fields': ['producto','fecha']}),
    ]
    extra = 1

class MascotaAdmin(admin.ModelAdmin):
    model = Mascota
    fieldsets = [
        ('Identificación de la Mascota', {'fields': ['propietario','nombre','raza',
                                                      'color','especie','edad','peso',
                                                      'descripcion','avatar']}),
        ('Anamnesis', {'fields': ['ambiental','alimento','bano']}),

    ]
    inlines = [VacunaInline,DesparacitanteInline]
    list_filter = ['created','modified']
    search_fields = ['ficha','nombre']

class EstadoMascotaAdmin(admin.ModelAdmin):
    model = EstadoMascota
    fieldsets = [
        ('Estado de la Mascota', {'fields': ['mascota','motivo','fr','fc','fp',
                                             't','exampiel','examucvis','gangpal',
                                             'apetito','sed','defecac','miccion']}),
    ]
    list_filter = ['created','modified']
    search_fields = ['fichaseg']

admin.site.register(Mascota, MascotaAdmin)
admin.site.register(EstadoMascota, EstadoMascotaAdmin)
