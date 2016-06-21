#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, render_to_response
from django.db.models import Q
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django_apps.home.views import LoginRequiredMixin
from django_apps.persona.models import Proveedor

from .models import CompraEmpresa
from .forms import CompraEmpresaForm

@login_required(login_url='home:login_empleado')
def search_compra(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(proveedor__razon_social__icontains=query)|
            Q(categoria__nombre__icontains=query)|
            Q(producto__nombre___icontains=query)|
            Q(cantidad__icontains=query)
        )
        results = CompraEmpresa.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("compras/search_compra.html", {
        "results": results,
        "query": query
    })

class ListaCompras(LoginRequiredMixin,ListView):
    model = CompraEmpresa
    context_object_name = 'listar_compras'
    paginate_by = 10
    template_name = 'compras/compras.html'

class Almacen(LoginRequiredMixin, ListView):
    model = CompraEmpresa
    context_object_name = 'listar_compras'
    paginate_by = 10
    template_name = 'compras/almacen.html'

class NuevaCompraProveedor(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = CompraEmpresa
    form_class = CompraEmpresaForm
    success_message = 'Se ha comprado %(cantidad)s %(producto)s del proveedor %(proveedor)s'
    pk_url_kwarg = 'compra_pk'
    template_name = 'compras/nueva_compra.html'

    def get_proveedor(self):
        return get_object_or_404(Proveedor, slug=self.kwargs.get('proveedor_slug'))

    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        initial['proveedor'] = self.get_proveedor()
        return initial

    # def get_success_url(self):
    #     return reverse('compras:detalle_compra', kwargs={'compra_pk':self.kwargs['compra_pk']})

class NuevaCompra(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = CompraEmpresa
    form_class = CompraEmpresaForm
    success_message = 'Se compró %(cantidad)s nuevos productos correctamente'
    template_name = 'compras/nueva_compra.html'
    pk_url_kwarg = 'compra_pk'

    # def get_success_url(self):
    #     return reverse('compras:detalle_compra', kwargs={'compra_pk':self.kwargs['compra_pk']})

class DetalleCompra(LoginRequiredMixin,DetailView):
    model = CompraEmpresa
    pk_url_kwarg = 'compra_pk'
    template_name = 'compras/detalle_compra.html'

class EditarCompra(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = CompraEmpresa
    form_class = CompraEmpresaForm
    success_message = 'Se ha editado la compra de %(producto.nombre)s del proveedor %(proveedor.razon_social)s'
    pk_url_kwarg = 'compra_pk'
    template_name = 'compras/nueva_compra.html'

class EliminarCompra(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = CompraEmpresa
    pk_url_kwarg = 'compra_pk'
    success_url = reverse_lazy('compras:listar_compras')
    success_message = 'Se eliminó el la compra de %(producto.nombre)s'
    template_name = 'compras/confirmar_eliminar_compra.html'
