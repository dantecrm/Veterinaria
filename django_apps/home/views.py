#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.views.generic import *
from django.conf import settings
from django.views.generic import FormView, TemplateView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import resolve_url
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from django.db.models import Q
from django.template.response import TemplateResponse
from registration.signals import user_registered
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from .models import Empleado
from .forms import CrearEmpleadoForm, EmpleadoEditForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

def setlanguage(request):
    context = {
        'LANGUAGES': settings.LANGUAGES,
        'SELECTEDLANG': request.LANGUAGE_CODE
    }
    return render(request, "set-languaje.html", context)

# HTTP Error 400
def bad_request(request):
    response = render_to_response(
        '400.html',
        context_instance=RequestContext(request)
    )
    response.status_code = 400
    return response

# HTTP Error 403
def permission_denied(request):
    response = render_to_response(
        '403.html',
        context_instance=RequestContext(request)
    )
    response.status_code = 400
    return response

# HTTP Error 404
def page_not_found(request):
    response = render_to_response(
        '404.html',
        context_instance=RequestContext(request)
    )
    response.status_code = 400
    return response

# HTTP Error 500
def server_error(request):
    response = render_to_response(
        '500.html',
        context_instance=RequestContext(request)
    )
    response.status_code = 400
    return response

@login_required(login_url='home:login_empleado')
def search_empleado(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(username__icontains=query)|
            Q(first_name__icontains=query)|
            Q(last_name__icontains=query)|
            Q(dni__icontains=query)
        )
        results = Empleado.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("home/search_empleado.html", {
        "results": results,
        "query": query
    })

class Login(FormView):
    form_class = AuthenticationForm
    template_name = "home/login.html"
    success_url = reverse_lazy('home:inicio')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


class Logout(RedirectView):
    pattern_name = 'home:login_empleado'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)

class LoginRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home:login_empleado'))
        else:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class ControlPanelVeterinaria(LoginRequiredMixin, TemplateView):
    template_name = 'base_sistema.html'
    def get_context_data(self, **kwargs):
        context = super(ControlPanelVeterinaria, self).get_context_data(**kwargs)
        context['empleados'] = Empleado.objects.all()
        return context

class CrearEmpleado(SuccessMessageMixin,FormView):
    model = Empleado
    form_class = CrearEmpleadoForm
    template_name = 'home/signup.html'
    success_url = reverse_lazy('home:login_empleado')
    success_message = 'El empleado %(username)s se ha creado correctamente'
    slug_url_kwarg = 'empleado_slug'

    def get_initial(self):
        logout(self.request)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        form.full_clean()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            empleado = Empleado.objects.create_user(username,email,password)
            empleado.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def EditarEmpleado(request, slug=None):
    """
    Editar usuario de forma simple.
    """
    user = request.user
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            #Actualizar el objeto
            user = form.save()
            messages.success(request, 'Usuario actualizado exitosamente.', extra_tags='html_dante')
            return HttpResponseRedirect(reverse('home:listar_empleados'))
    else:
        form = UserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'home/empleado_form.html', context)

class EditarEmpleado(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    model = Empleado
    form_class = EmpleadoEditForm
    template_name = 'home/empleado_form.html'
    success_message = 'El empleado %(first_name)s se ha editado correctamente'
    slug_url_kwarg = 'empleado_slug'

    def get_success_url(self):
        return reverse('home:detalle_empleado', kwargs={'empleado_slug':self.object.slug})

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(EditUser, self).dispatch(*args, **kwargs)

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='home/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    empleado_slug=None,
                    extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('home:login_empleado')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            messages.success(request, _('Contrasena cambiado correctamente'),extra_tags='html_dante')
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    return TemplateResponse(request, template_name, context)


class ListaEmpleados(LoginRequiredMixin,ListView):
    model = Empleado
    context_object_name = 'list_empleados'
    template_name = 'home/listar_empleados.html'
    paginate_by = 10

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ListaEmpleados, self).dispatch(*args, **kwargs)

class DetalleEmpleado(LoginRequiredMixin,DetailView):
    model = Empleado
    template_name = 'home/detalle_empleado.html'
    slug_url_kwarg = 'empleado_slug'

class EliminarEmpleado(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'home/confirmar_eliminar_empleado.html'
    slug_url_kwarg = 'empleado_slug'
    success_url = reverse_lazy('home:listar_empleados')
