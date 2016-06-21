#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.db.models import Q
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django_apps.home.views import LoginRequiredMixin
from .models import Cliente, Proveedor
from .forms import ClienteForm, ProveedorForm

@login_required(login_url='home:login_empleado')
def search_cliente(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre__icontains=query)|
            Q(ap_pater__icontains=query)|
            Q(ap_pater__icontains=query)|
            Q(dni__icontains=query)|
            Q(sexo__icontains=query)
        )
        results = Cliente.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("persona/search_cliente.html", {
        "results": results,
        "query": query
    })

@login_required(login_url='home:login_empleado')
def search_proveedor(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(razon_social__icontains=query)|
            Q(ruc__icontains=query)|
            Q(contacto__icontains=query)|
            Q(email__icontains=query)
        )
        results = Proveedor.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("persona/search_proveedor.html", {
        "results": results,
        "query": query
    })

class ListaClientes(LoginRequiredMixin,ListView):
    model = Cliente
    context_object_name = 'listar_clientes'
    template_name = 'persona/clientes.html'

class CrearCliente(CreateView,LoginRequiredMixin,SuccessMessageMixin):
    model = Cliente
    form_class = ClienteForm
    template_name = 'persona/crear_cliente.html'
    success_message = 'El Cliente %(nombre)s se ha creado correctamente'
    slug_url_kwarg = 'cliente_slug'

class DetalleCliente(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'persona/detalle_cliente.html'
    slug_url_kwarg = 'cliente_slug'

class EditarCliente(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Cliente
    form_class = ClienteForm
    success_message = 'El Cliente %(nombre)s se ha editado correctamente'
    template_name = 'persona/crear_cliente.html'
    slug_url_kwarg = 'cliente_slug'

class EliminarCliente(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Cliente
    slug_url_kwarg = 'cliente_slug'
    warning_message = 'El Cliente %(nombre)s se eliminó correctamente'
    success_url = reverse_lazy('persona:listar_clientes')
    template_name = 'persona/confirmar_eliminar_cliente.html'

class ListaProveedores(LoginRequiredMixin,ListView):
    model = Proveedor
    context_object_name = 'listar_proveedores'
    template_name = 'persona/proveedores.html'

class CrearProveedor(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Proveedor
    form_class = ProveedorForm
    slug_url_kwarg = 'proveedor_slug'
    success_message = 'El proveedor %(razon_social)s se ha creado correctamente'
    template_name = 'persona/crear_proveedor.html'

class DetalleProveedor(LoginRequiredMixin,DetailView):
    model = Proveedor
    template_name = 'persona/detalle_proveedor.html'
    slug_url_kwarg = 'proveedor_slug'

class EditarProveedor(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    slug_url_kwarg = 'proveedor_slug'
    success_message = 'El proveedor %(razon_social)s se ha editado correctamente'
    template_name = 'persona/crear_proveedor.html'

class EliminarProveedor(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Proveedor
    success_url = reverse_lazy('persona:listar_proveedores')
    warning_message = 'El proveedor %(razon_social)s se ha eliminado correctamente'
    slug_url_kwarg = 'proveedor_slug'
    template_name = 'persona/confirmar_eliminar_proveedor.html'

