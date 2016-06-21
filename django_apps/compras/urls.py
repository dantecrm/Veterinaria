# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

app_name = 'compras'

urlpatterns = [
    url(r'^$', views.ListaCompras.as_view(), name='listar_compras'),
    url(r'^search-compra/$', views.search_compra, name="buscar_compra"),
    url(r'^almacen/$', views.Almacen.as_view(), name='almacen'),
    url(r'^(?P<proveedor_slug>[\w-]+)/nueva-compra/$', views.NuevaCompraProveedor.as_view(), name='nueva_compra_proveedor'),
    url(r'^nueva-compra/$', views.NuevaCompra.as_view(), name='nueva_compra'),
    url(r'^(?P<compra_pk>[0-9]+)/$', views.DetalleCompra.as_view(), name='detalle_compra'),
    url(r'^(?P<compra_pk>[0-9]+)/editar/$', views.EditarCompra.as_view(), name='editar_compra'),
    url(r'^(?P<compra_pk>[0-9]+)/eliminar/$', views.EliminarCompra.as_view(), name='eliminar_compra'),
]
