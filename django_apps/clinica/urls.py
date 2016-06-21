# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

app_name = 'clinica'

urlpatterns = [
    #Lista de Propietarios
    url(r'^propietarios/$', views.ClienteClinico.as_view(), name='propietarios'),
    #Busquedas
    url(r'^buscar-propietario/$', views.search_propietario, name='buscar_propietario'),
    url(r'^(?P<cliente_slug>[\w-]+)/buscar-mascota/$', views.search_mascota, name='buscar_mascota'),
    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/buscar-historial/$', views.search_historial, name='buscar_historial'),
    # Mantenimiento de Mascotas del cliente o propietario
    url(r'^(?P<cliente_slug>[\w-]+)/mascotas/$', views.ListaMascotas.as_view(), name='listar_mascotas'),
    url(r'^(?P<cliente_slug>[\w-]+)/agregar-mascota/$', views.NuevaMascota, name='agregar_mascota'),
    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/$', views.DetalleMascota.as_view(), name='detalle_mascota'),
    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/editar/$', views.EditarMascota, name='editar_mascota'),
    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/eliminar/$', views.EliminarMascota.as_view(), name='eliminar_mascota'),
    # url(r'^(?P<cliente_slug>[\w-]+)/nueva-mascota/$', views.NuevaMascota.as_view(), name='nueva_mascota'),
    # url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/editar/$', views.EditarMascota.as_view(), name='editar_mascota'),

    # Mantenimiento de Estados de las mascotas de los clientes
    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/historial/$',
        views.HistorialMascota.as_view(), name='historial_mascota'),

    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/nuevo-historial/$',
        views.NuevoEstadoMascota.as_view(), name='nuevo_estado_mascota'),

    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/(?P<estado_slug>[\w-]+)/$',
        views.DetalleEstadoMascota.as_view(), name='detalle_estado_mascota'),

    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/(?P<estado_slug>[\w-]+)/editar/$',
        views.EditarEstadoMascota.as_view(), name='editar_estado_mascota'),

    url(r'^(?P<cliente_slug>[\w-]+)/(?P<mascota_slug>[\w-]+)/(?P<estado_slug>[\w-]+)/eliminar/$',
        views.EliminarEstadoMascota.as_view(),name='eliminar_estado_mascota'),
]
