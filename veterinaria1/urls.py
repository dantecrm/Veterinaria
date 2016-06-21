# -*- coding: utf-8 -*-
"""veterinaria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, patterns, url, i18n
from django.conf.urls import (
    handler400, handler403, handler404, handler500
)
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django_apps.home import views
import ajax_select

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include('django_apps.home.urls')),
    url(r'^persona/', include('django_apps.persona.urls')),
    url(r'^inventario/', include('django_apps.inventario.urls')),
    url(r'^compras/', include('django_apps.compras.urls')),
    url(r'^ventas/', include('django_apps.ventas.urls')),
    url(r'^clinica/', include('django_apps.clinica.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^ajax-select/', include('ajax_select.urls')),
    # url(r'^rosetta/', include('rosetta.urls')),
    url(r'^$', views.setlanguage, name='setlanguage'),

    #Gestion de Usuarios Empleados

    # url(r'^logout/$', views.logout_view, name='logout_empleado'),

    ## Gestion de Perfiles de Usuarios Empleados
    # url(r'^empleado/(?P<pk>[0-9]+)/$', views.DetailPerfilEmpleado.as_view(),
    #     name='detalle_perfil_empleado'),
    # url(r'^empleado/(?P<pk>[0-9]+)/editar/$', views.ActualizarPerfilEmpleado.as_view(),
    #     name='editar_perfil_empleado'),

]
handler400 = 'django_apps.home.views.bad_request'
handler403 = 'django_apps.home.views.permission_denied'
handler404 = 'django_apps.home.views.page_not_found'
handler500 = 'django_apps.home.views.server_error'

urlpatterns += i18n_patterns(
    url(r'^$', views.setlanguage, name='setlanguage'),
    # url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^persona/', include('django_apps.persona.urls')),
    url(r'^inventario/', include('django_apps.inventario.urls')),
    url(r'^compras/', include('django_apps.compras.urls')),
    url(r'^ventas/', include('django_apps.ventas.urls')),
    url(r'^clinica/', include('django_apps.clinica.urls')),
    # url(r'^', include('django_apps.home.urls')),
    # url(r'^ajax-select/', include('ajax_select.urls')),
)


# handler404 = 'views.Page_not_Found'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

