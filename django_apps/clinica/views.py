#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.context_processors import csrf
from django.template import RequestContext # For CSRF
from django.db.models import Q
from django.views.generic import FormView, TemplateView, RedirectView
from django.forms.formsets import formset_factory, BaseFormSet
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic import *
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django_apps.home.views import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import BaseInlineFormSet
from django.utils.decorators import method_decorator
from django.forms.models import inlineformset_factory

from django_apps.persona.models import Cliente
from .models import Mascota,Vacuna,Desparacitante,EstadoMascota
from .forms import MascotaForm, VacunaForm, VacunaFormSet, DesparacitanteForm, DesparacitanteFormSet, EstadoMascotaForm

@login_required(login_url='home:login_empleado')
def search_propietario(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(id__icontains=query)|
            Q(nombre__icontains=query)|
            Q(ap_pater__icontains=query)|
            Q(ap_mater__icontains=query)|
            Q(dni__icontains=query)
        )
        results = Cliente.objects.filter(qset).distinct()
        mascotas = Mascota.objects.all()
    else:
        results = []
    return render_to_response("clinica/search_propietario.html", {
        "results": results,
        "mascotas" : mascotas,
        "query": query
    })

@login_required(login_url='home:login_empleado')
def search_mascota(request, cliente_slug=None):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(id__icontains=query)|
            Q(propietario__nombre__icontains=query)|
            Q(propietario__ap_pater__icontains=query)|
            Q(propietario__ap_mater__icontains=query)|
            Q(ficha__icontains=query)|
            Q(nombre__icontains=query)|
            Q(raza__icontains=query)|
            Q(color__icontains=query)|
            Q(especie__icontains=query)|
            Q(edad__icontains=query)|
            Q(peso__icontains=query)
        )
        results = Mascota.objects.filter(qset).distinct()
        cliente = Cliente.objects.get(slug=cliente_slug)
    else:
        results = []
    return render_to_response("clinica/search_mascota.html", {
        "results": results,
        "cliente": cliente,
        "query": query
    })

@login_required(login_url='home:login_empleado')
def search_historial(request, cliente_slug=None,mascota_slug=None):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(id__icontains=query)|
            Q(created__icontains=query)|
            Q(motivo__icontains=query)|
            Q(fichaseg__icontains=query)
        )
        results = EstadoMascota.objects.filter(qset).distinct()
        mascota = Mascota.objects.get(slug=mascota_slug)
    else:
        results = []
    return render_to_response("clinica/search_historial.html", {
        "results": results,
        "mascota": mascota,
        "query": query
    })

class ClienteClinico(LoginRequiredMixin, TemplateView):
    template_name = 'clinica/clientes_clinicos.html'
    slug_url_kwarg = 'mascota_slug'

    def get_context_data(self, **kwargs):
        context = super(ClienteClinico, self).get_context_data(**kwargs)
        context['clientes'] = Cliente.objects.all()
        context['mascotas'] = Mascota.objects.all()
        return context

class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        self.validate_unique()
        if any(self.errors):
            return
        if not self.forms[0].has_changed():
            raise forms.ValidationError("At least one %s is required" % self.model._meta.verbose_name)

@login_required(login_url='home:login_empleado')
def NuevaMascota(request, cliente_slug):
    # def get_cliente(self):
    #     return get_object_or_404(Cliente, slug=self.kwargs.get('cliente_slug'))

    # def get_initial(self):
    #     initial = super(OrdenVentaForm, self).get_initial()
    #     initial['propietario'] = self.get_propietario()
    #     return initial
    mascota_form = MascotaForm(request.POST or None, request.FILES or None)
    VacunaFormSet = inlineformset_factory(Mascota, Vacuna, form=VacunaForm,formset=RequiredBaseInlineFormSet, max_num=10, extra=1)
    vacuna_formset = VacunaFormSet(request.POST or None, prefix='vacuna')
    DesparacitanteFormSet = inlineformset_factory(Mascota, Desparacitante, form=DesparacitanteForm,formset=RequiredBaseInlineFormSet, max_num=10, extra=1)
    desparacitante_formset = DesparacitanteFormSet(request.POST or None, prefix='desparacitante')
    if mascota_form.is_valid() and vacuna_formset.is_valid() and desparacitante_formset.is_valid():
        mascota = mascota_form.save()
        vacuna = vacuna_formset.save(commit=False)
        desparacitante = desparacitante_formset.save(commit=False)
        for v in vacuna:
            v.mascota = mascota
            v.save()
        for d in desparacitante:
            d.mascota = mascota
            d.save()
        messages.add_message(request, messages.INFO, 'Mascota registrado correctamente')
        return HttpResponseRedirect(mascota.get_absolute_url())
    context = {
            'form': mascota_form,
            'vacuna_form':vacuna_formset,
            'desparacitante_form':desparacitante_formset,
    }
    return render_to_response(
        'clinica/crear_mascota.html', context, context_instance = RequestContext(request)
    )

class ListaMascotas(LoginRequiredMixin, ListView):
    model = Mascota
    paginate_by = 10
    context_object_name = 'listar_mascotas'
    template_name = 'clinica/mascotas.html'
    slug_url_kwarg = 'cliente_slug'

    def get_context_data(self, **kwargs):
        context = super(ListaMascotas,self).get_context_data(**kwargs)
        context['cliente'] = Cliente.objects.get(slug=self.kwargs['cliente_slug'])
        context['historial_mascota'] = EstadoMascota.objects.all()
        return context

@login_required(login_url='home:login_empleado')
def EditarMascota(request, cliente_slug, mascota_slug):
    instance = Mascota.objects.get(slug=mascota_slug)
    mascota_form = MascotaForm(request.POST or None, request.FILES or None, instance=instance)
    VacunaFormSet = inlineformset_factory(Mascota, Vacuna, form=VacunaForm,formset=RequiredBaseInlineFormSet, max_num=10, extra=1)
    vacuna_formset = VacunaFormSet(request.POST or None, prefix='vacuna',instance=instance)
    DesparacitanteFormSet = inlineformset_factory(Mascota, Desparacitante, form=DesparacitanteForm,formset=RequiredBaseInlineFormSet, max_num=10, extra=1)
    desparacitante_formset = DesparacitanteFormSet(request.POST or None, prefix='desparacitante',instance=instance)
    if mascota_form.is_valid() and vacuna_formset.is_valid() and desparacitante_formset.is_valid():
        mascota = mascota_form.save()
        vacuna = vacuna_formset.save(commit=False)
        desparacitante = desparacitante_formset.save(commit=False)
        for v in vacuna:
            v.mascota = mascota
            v.save()
        for d in desparacitante:
            d.mascota = mascota
            d.save()
        messages.add_message(request, messages.INFO, 'Mascota editado correctamente')
        return HttpResponseRedirect(mascota.get_absolute_url())
    context = {
            'form': mascota_form,
            'vacuna_form':vacuna_formset,
            'desparacitante_form':desparacitante_formset,
    }
    return render_to_response(
        'clinica/crear_mascota.html', context, context_instance = RequestContext(request)
    )

class DetalleMascota(LoginRequiredMixin, DetailView):
    model = Mascota
    template_name = 'clinica/detalle_mascota.html'
    slug_url_kwarg = 'mascota_slug'

    def get_context_data(self,**kwargs):
        context = super(DetalleMascota, self).get_context_data(**kwargs)
        context['vacunas'] = Vacuna.objects.filter(mascota_id=self.object.id)
        # context['vacuna'] = Vacuna.objects.filter(pk=self.kwargs['mascota_slug'])
        context['desparacitantes'] = Desparacitante.objects.filter(mascota_id=self.object.id)
        return context

class EliminarMascota(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Mascota
    success_message = 'La mascota %(nombre)s se ha eliminado de la base de datos'
    slug_url_kwarg = 'mascota_slug'
    template_name = 'clinica/confirmar_eliminar_mascota.html'
    def get_success_url(self):
        return reverse('clinica:listar_mascotas', kwargs={'cliente_slug':self.kwargs['cliente_slug']})

class HistorialMascota(LoginRequiredMixin, ListView):
    model = EstadoMascota
    paginate_by = 10
    context_object_name = 'historial_mascota'
    template_name = 'clinica/historial_clinico_mascota.html'
    slug_url_kwarg = 'mascota_slug'

    def get_context_data(self, **kwargs):
        context = super(HistorialMascota,self).get_context_data(**kwargs)
        context['mascota'] = Mascota.objects.get(slug=self.kwargs['mascota_slug'])
        return context

class NuevoEstadoMascota(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = EstadoMascota
    form_class = EstadoMascotaForm
    success_message = 'Se ha agregado un nuevo estado actual de la mascota %(mascota)s'
    slug_url_kwarg = 'mascota_slug'
    template_name = 'clinica/nuevo_estado_mascota.html'

    def get_mascota(self):
        return get_object_or_404(Mascota, slug=self.kwargs.get('mascota_slug'))

    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        initial['mascota'] = self.get_mascota()
        return initial

    def get_context_data(self, **kwargs):
        context = super(NuevoEstadoMascota,self).get_context_data(**kwargs)
        context['mascota'] = Mascota.objects.get(slug=self.kwargs['mascota_slug'])
        return context

class DetalleEstadoMascota(LoginRequiredMixin,DetailView):
    model = EstadoMascota
    slug_url_kwarg = 'estado_slug'
    template_name = 'clinica/detalle_estado_mascota.html'

class EditarEstadoMascota(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = EstadoMascota
    form_class = EstadoMascotaForm
    success_message = 'Se ha editado correctament el estado actual n° %(fichaseg)s del paciente %(mascota.nombre)s'
    slug_url_kwarg = 'estado_slug'
    template_name = 'clinica/nuevo_estado_mascota.html'

class EliminarEstadoMascota(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = EstadoMascota
    success_message = 'Se ha eliminado correctament el estado N°:%(fichaseg)s del paciente %(mascota.nombre)s'
    slug_url_kwarg = 'estado_slug'
    template_name = 'clinica/confirmar_eliminar_estado_mascota.html'

    def get_success_url(self):
        # return reverse('clinica:historial_mascota', kwargs={'cliente_slug':self.object.mascota.propietario.slug,'mascota_slug':self.kwargs['mascota_slug']})
        return reverse('clinica:historial_mascota', kwargs={'cliente_slug':self.object.mascota.propietario.slug,'mascota_slug':self.object.mascota.slug})

# class NuevaMascota(LoginRequiredMixin,SuccessMessageMixin,CreateView):
#     model = Mascota
#     form_class = MascotaForm
#     success_message = 'La mascota %(nombre)s se ha agregado correctamente al registro'
#     slug_url_kwarg = 'mascota_slug'
#     # pk_url_kwarg = 'mascota_pk'
#     template_name = 'clinica/nueva_mascota.html'

#     def get(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         vacuna_form = VacunaFormSet(instance = self.object)
#         desparacitante_form = DesparacitanteFormSet(instance = self.object)
#         return self.render_to_response(self.get_context_data(form = form,
#                                                              vacuna_form = vacuna_form,
#                                                              desparacitante_form = desparacitante_form))
#     def post(self, request, *args, **kwargs):
#         self.object = None
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         vacuna_form = VacunaFormSet(request.POST or None,prefix='vacuna',)
#         desparacitante_form = DesparacitanteFormSet(request.POST or None, prefix='desparacitante')
#         if (form.is_valid() and vacuna_form.is_valid() and desparacitante_form.is_valid()):
#             # self.object = form.save()
#             # vacuna = vacuna_form.save(commit=False)
#             # desparacitante = desparacitante_form.save(commit=False)
#             # for form in vacuna:
#             #     form.instance = instance
#             #     form.save()

#             # for form in desparacintante:
#             #     form.instance = instance
#             #     form.save()
#             return self.form_valid(form, vacuna_form, desparacitante_form)
#         else:
#             return self.form_invalid(form, vacuna_form, desparacitante_form)

#     def form_valid(self, form, vacuna_form, desparacitante_form):
#         self.object = form.save()
#         vacuna_form.instance = self.object
#         vacuna_form.save()
#         desparacitante_form.instance = self.object
#         desparacitante_form.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form, vacuna_form, desparacitante_form):
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   vacuna_form=vacuna_form,
#                                   desparacitante_form=desparacitante_form)
#         )

# class EditarMascota(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = Mascota
#     form_class = MascotaForm
#     success_message = 'La mascota %(nombre)s se ha editado correctamente'
#     slug_url_kwarg = 'mascota_slug'
#     # pk_url_kwarg = 'mascota_pk'
#     template_name = 'clinica/nueva_mascota.html'

#     def get(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         vacuna_form = VacunaFormSet(instance = self.object)
#         desparacitante_form = DesparacitanteFormSet(instance = self.object)
#         return self.render_to_response(self.get_context_data(form = form,
#                                                              vacuna_form = vacuna_form,
#                                                              desparacitante_form = desparacitante_form))
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         vacuna_form = VacunaFormSet(self.request.POST)
#         desparacitante_form = DesparacitanteFormSet(self.request.POST)
#         if (form.is_valid() and vacuna_form.is_valid() and desparacitante_form.is_valid()):
#             return self.form_valid(form, vacuna_form, desparacitante_form)
#         else:
#             return self.form_invalid(form, vacuna_form, desparacitante_form)

#     def form_valid(self, form, vacuna_form, desparacitante_form):
#         self.object = form.save()
#         # for form in vacuna_form.forms:
#         #     vacuna = form.save(commit=False)
#         #     vacuna.instance = self.object
#         #     vacuna.save()

#         # for form in desparacintante_formset.forms:
#         #     desparacitante = form.save(commit=False)
#         #     desparacitante.instance = self.object
#         #     desparacitante.save()
#         vacuna_form.instance = self.object
#         vacuna_form.save()
#         desparacitante_form.instance = self.object
#         desparacitante_form.save()
#         return HttpResponseRedirect(self.get_success_url())

#     def form_invalid(self, form, vacuna_form, desparacitante_form):
#         return self.render_to_response(
#             self.get_context_data(form=form,
#                                   vacuna_form=vacuna_form,
#                                   desparacitante_form=desparacitante_form))
