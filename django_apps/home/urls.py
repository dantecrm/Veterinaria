# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
from django.conf import settings
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.urlresolvers import reverse_lazy
from . import views

app_name = 'home'

urlpatterns = [
    ## Gestion de usuarios
    url(r'^login/$', views.Login.as_view(), name='login_empleado'),
    url(r'^logout/$', views.Logout.as_view(), name='logout_empleado'),
    url(r'^veterinaria/$', views.ControlPanelVeterinaria.as_view(), name='inicio'),
    url(r'^empleados/$', views.ListaEmpleados.as_view(), name='listar_empleados'),
    url(r'^search-empleado/$', views.search_empleado, name="buscar_empleado"),
    url(r'^signup/$', views.CrearEmpleado.as_view(), name='signup_empleado'),
    url(r'^(?P<empleado_slug>[\w-]+)/$', views.DetalleEmpleado.as_view(), name='detalle_empleado'),

    #Cambiar Usuario creado
    # url(r'^usuario/(?P<pk>[0-9]+)/editar/$', views.EditUser,
    #     name="editar_user"),
    url(r'^(?P<empleado_slug>[\w-]+)/editar/$', views.EditarEmpleado.as_view(),
        name="editar_empleado"),

    url(r'^(?P<empleado_slug>[\w-]+)/eliminar/$', views.EliminarEmpleado.as_view(),
        name="eliminar_empleado"),
    # Cambiar Contraseña de usuario
    # url(r'^usuarios/', include('django.contrib.auth.urls')),
    url(r'^(?P<empleado_slug>[\w-]+)/password_change/$', views.password_change,
        name="password_change"),

]

