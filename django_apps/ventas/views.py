#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.context_processors import csrf
from django.db.models import Q
from django.template import RequestContext
from django.conf import settings
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect, Http404
from wkhtmltopdf.views import PDFTemplateResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django_apps.home.views import LoginRequiredMixin
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory

from django.contrib import messages
from .models import OrdenVenta, CarritoVenta
from .forms import OrdenVentaForm, CarritoVentaForm, CarritoVentaFormset

@login_required(login_url='home:login_empleado')
def search_venta(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(id__icontains=query)|
            Q(codigo__icontains=query)|
            Q(cliente__nombre__icontains=query)|
            Q(cliente__ap_pater__icontains=query)|
            Q(cliente__ap_mater__icontains=query)
        )
        results = OrdenVenta.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("ventas/search_venta.html", {
        "results": results,
        "query": query
    })

class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        self.validate_unique()
        if any(self.errors):
            return
        if not self.forms[0].has_changed():
            raise forms.ValidationError("At least one %s is required" % self.model._meta.verbose_name)

@login_required(login_url='home:login_empleado')
def CreateVenta(request):
    venta_form = OrdenVentaForm(request.POST or None)
    CarritoFormSet = inlineformset_factory(OrdenVenta, CarritoVenta, form=CarritoVentaForm,formset=RequiredBaseInlineFormSet, max_num=10, extra=1)
    carrito_formset = CarritoFormSet(request.POST or None, prefix='carrito')
    if venta_form.is_valid() and carrito_formset.is_valid():
        venta = venta_form.save()
        carrito = carrito_formset.save(commit=False)
        for producto in carrito:
            producto.venta = venta
            producto.save()
        messages.add_message(request, messages.INFO, 'Venta efectuada correctamente')
        return HttpResponseRedirect(venta.get_absolute_url())
    return render_to_response(
        'ventas/venta_form.html', {
            'form': venta_form,
            'formset':carrito_formset,
        }, context_instance = RequestContext(request)
    )


@login_required(login_url='home:login_empleado')
def UpdateVenta(request, venta_pk=None):
    # if not request.user.is_staff or not request.user.is_superuser:
    #     raise Http404
    instance = OrdenVenta.objects.get(pk=venta_pk)
    venta_form = OrdenVentaForm(request.POST or None, instance=instance)
    CarritoFormSet = inlineformset_factory(OrdenVenta, CarritoVenta, form=CarritoVentaForm,formset=RequiredBaseInlineFormSet, max_num=10, extra=1)
    carrito_formset = CarritoFormSet(request.POST or None, prefix='carrito', instance=instance)
    if venta_form.is_valid() and carrito_formset.is_valid():
        venta = venta_form.save()
        carrito = carrito_formset.save(commit=False)
        for producto in carrito:
            producto.venta = venta
            producto.save()
        messages.add_message(request, messages.INFO, 'Venta editada correctamente')
        return HttpResponseRedirect(venta.get_absolute_url())
    return render_to_response(
        'ventas/venta_form.html', {
            'form': venta_form,
            'formset':carrito_formset,
        }, context_instance = RequestContext(request)
    )

class ListaVentas(LoginRequiredMixin,ListView):
    model = OrdenVenta
    paginate_by = 10
    context_object_name = 'listar_ventas'
    template_name = 'ventas/ventas.html'

class DetalleVenta(LoginRequiredMixin,DetailView):
    model = OrdenVenta
    template_name = 'ventas/detalle_venta.html'
    pk_url_kwarg = 'venta_pk'

    def get_context_data(self, **kwargs):
        context = super(DetalleVenta, self).get_context_data(**kwargs)
        # context['productos'] = CarritoVenta.objects.get(pk=self.kwargs.get('venta_pk',None))
        context['productos'] = CarritoVenta.objects.filter(venta_id=self.object.id)
        a = CarritoVenta.objects.all().values()
        t = 0
        for j in range(len(a)):
            if self.object.id == a[j].get('venta_id'):
                t += float(a[j].get('total'))
        context['total_venta'] = t
        return context

class VentaPDF(DetailView):
    model = OrdenVenta
    pk_url_kwarg = 'venta_pk'
    template='ventas/venta_pdf.html'
    context= {'title': 'Detalle de Venta'}


    def get(self, request, *args, **kwargs):
        self.context['venta'] = self.get_object()
        self.context['productos'] = CarritoVenta.objects.filter(venta_id=self.get_object().id)
        a = CarritoVenta.objects.all().values()
        t = 0
        for j in range(len(a)):
            if self.get_object().id == a[j].get('venta_id'):
                t += float(a[j].get('total'))
        self.context['total_venta'] = t

        response=PDFTemplateResponse(request=request,
                                     template=self.template,
                                     # filename ="venta.pdf",
                                     context=self.context,
                                     show_content_in_browser=False,
                                     # cmd_options=settings.WKHTMLTOPDF_CMD_OPTIONS,
                                     )
        return response

class EliminarVenta(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = OrdenVenta
    pk_url_kwarg = 'venta_pk'
    success_url = reverse_lazy('ventas:listar_ventas')
    success_message = 'La venta se eliminó con éxito'
    template_name = 'ventas/confirmar_eliminar_venta.html'

# class NuevaVenta(LoginRequiredMixin,SuccessMessageMixin,CreateView):
#     model = OrdenVenta
#     form_class = OrdenVentaForm
#     success_message = 'La venta se realizó correctamente'
#     pk_url_kwarg = 'venta_pk'
#     template_name = 'ventas/nueva_venta.html'

#     def get(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         carrito_form = CarritoVentaFormset(instance = self.object)
#         return self.render_to_response(self.get_context_data(form = form, carrito_form = carrito_form))

#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         carrito_form = CarritoVentaFormset(self.request.POST, prefix='carrito')
#         if (form.is_valid() and carrito_form.is_valid()):
#             return self.form_valid(form, carrito_form)
#         else:
#             return self.form_invalid(form, carrito_form)

#     def form_valid(self, form, carrito_form):
#         self.object = form.save()
#         carrito_form.instance = self.object
#         carrito_form.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form, carrito_form):
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   carrito_form=carrito_form)
#         )

# class EditarVenta(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
#     template_name = 'ventas/nueva_venta.html'
#     model = OrdenVenta
#     success_message = 'La venta se editó correctamente'
#     pk_url_kwarg = 'venta_pk'
#     form_class = OrdenVentaForm

#     # def get_context_data(self, **kwargs):
#     #     context = super(EditarVenta, self).get_context_data(**kwargs)
#     #     if self.request.POST:
#     #         context['form'] = OrdenVentaForm(self.request.POST, instance=self.object)
#     #         context['carrito_form'] = CarritoVentaFormset(self.request.POST, instance=self.object)
#     #     else:
#     #         context['form'] = RecipeForm(instance=self.object)
#     #         context['carrito_form'] = CarritoVentaFormset(instance=self.object)
#     #     return context
#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         carrito_form = CarritoVentaFormset(instance = self.object)
#         return self.render_to_response(self.get_context_data(form = form,
#                                                              carrito_form = carrito_form))

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         carrito_form = CarritoVentaFormset(self.request.POST, prefix='carrito')
#         if (form.is_valid() and carrito_form.is_valid()):
#             return self.form_valid(form, carrito_form)
#         else:
#             return self.form_invalid(form, carrito_form)

#     def form_valid(self, form, carrito_form):
#         self.object = form.save()
#         carrito_form.instance = self.object
#         carrito_form.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form, carrito_form):
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   carrito_form=carrito_form)
#         )
