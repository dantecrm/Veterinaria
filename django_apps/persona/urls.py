# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

app_name = 'persona'

urlpatterns = [
    url(r'^search-cliente/$', views.search_cliente, name="buscar_cliente"),
    url(r'^clientes/$', views.ListaClientes.as_view(), name='listar_clientes'),
    url(r'^cliente/crear/$', views.CrearCliente.as_view(), name='crear_cliente'),
    url(r'^cliente/(?P<cliente_slug>[\w-]+)/$', views.DetalleCliente.as_view(), name='detalle_cliente'),
    url(r'^cliente/(?P<cliente_slug>[\w-]+)/editar/$', views.EditarCliente.as_view(), name='editar_cliente'),
    url(r'^cliente/(?P<cliente_slug>[\w-]+)/eliminar/$', views.EliminarCliente.as_view(), name='eliminar_cliente'),

    url(r'^search-proveedor/$', views.search_proveedor, name="buscar_proveedor"),
    url(r'^proveedores/$', views.ListaProveedores.as_view(), name='listar_proveedores'),
    url(r'^proveedor/crear/$', views.CrearProveedor.as_view(), name='crear_proveedor'),
    url(r'^proveedor/(?P<proveedor_slug>[\w-]+)/$', views.DetalleProveedor.as_view(), name='detalle_proveedor'),
    url(r'^proveedor/(?P<proveedor_slug>[\w-]+)/editar/$', views.EditarProveedor.as_view(), name='editar_proveedor'),
    url(r'^proveedor/(?P<proveedor_slug>[\w-]+)/eliminar/$', views.EliminarProveedor.as_view(), name='eliminar_proveedor'),
]
