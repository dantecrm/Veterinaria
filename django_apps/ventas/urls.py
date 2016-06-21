from django.conf.urls import include, url
from . import views

app_name = 'ventas'

urlpatterns = [
    url(r'^$', views.ListaVentas.as_view(), name='listar_ventas'),
    url(r'^search-venta/$', views.search_venta, name='buscar_venta'),
    # url(r'^nuevo/$', views.NuevaVenta, name='nueva_venta'),
    url(r'^nueva-venta/$', views.CreateVenta, name='venta_nueva'),
    url(r'^(?P<venta_pk>[0-9]+)/editar-venta/$', views.UpdateVenta, name='update_venta'),
    url(r'^(?P<venta_pk>[0-9]+)/$', views.DetalleVenta.as_view(), name='detalle_venta'),
    # url(r'^(?P<venta_pk>[0-9]+)/editar/$', views.EditarVenta.as_view(), name='editar_venta'),
    url(r'^(?P<venta_pk>[0-9]+)/eliminar/$', views.EliminarVenta.as_view(), name='eliminar_venta'),
]
