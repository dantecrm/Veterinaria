# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from . import views

app_name = 'inventario'

urlpatterns = [
    #Búsquedas de articulos
    url(r'^search-articulo/$', views.search_articulo, name="buscar_articulo"),
    #CRUD de Articulos
    url(r'^articulos/$', views.ListarArticulos.as_view(), name='listar_articulos'),
    url(r'^articulo/crear/$', views.CrearArticulo.as_view(), name='crear_articulo'),
    url(r'^articulo/(?P<articulo_slug>[\w-]+)/$', views.DetalleArticulo.as_view(), name='detalle_articulo'),
    url(r'^articulo/(?P<articulo_slug>[\w-]+)/editar/$', views.EditarArticulo.as_view(), name='editar_articulo'),
    url(r'^articulo/(?P<articulo_slug>[\w-]+)/eliminar/$', views.EliminarArticulo.as_view(), name='eliminar_articulo'),
    #Búsquedas de Categorias
    url(r'^search-categoria/$', views.search_categoria, name="buscar_categoria"),
    #CRUD de Categorias
    url(r'^categorias/$', views.ListarCategorias.as_view(), name='listar_categorias'),
    url(r'^categoria/crear/$', views.CrearCategoria.as_view(), name='crear_categoria'),
    url(r'^categoria/(?P<categoria_slug>[\w-]+)/editar/$', views.EditarCategoria.as_view(), name='editar_categoria'),
    url(r'^categoria/(?P<categoria_slug>[\w-]+)/eliminar/$', views.EliminarCategoria.as_view(), name='eliminar_categoria'),
]
