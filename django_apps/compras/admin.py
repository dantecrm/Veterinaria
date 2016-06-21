from django.contrib import admin
from .models import CompraEmpresa

class CompraEmpresaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Nueva Compra de la Empresa', {'fields': ['proveedor','categoria','producto','cantidad','afecto','descuento']}),
    ]
admin.site.register(CompraEmpresa, CompraEmpresaAdmin)
