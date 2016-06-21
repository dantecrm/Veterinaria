from django.contrib import admin
from .models import OrdenVenta, CarritoVenta

class CarritoVentaInline(admin.TabularInline):
    model = CarritoVenta
    fieldsets = [
        ('Eleccion de Productos', {'fields': ['producto','cantidad']}),
    ]
    extra = 1

class OrdenVentaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Elegir Cliente', {'fields': ['cliente']}),
    ]
    inlines = [CarritoVentaInline]
    list_filter = ['created','modified']
    search_fields = ['codigo']

admin.site.register(OrdenVenta,OrdenVentaAdmin)
