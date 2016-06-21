from django.shortcuts import render, render_to_response
from django.db.models import Q
from django.views.generic import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django_apps.home.views import LoginRequiredMixin
from .models import Articulo, Categoria
from .forms import ArticuloForm, CategoriaForm

@login_required(login_url='home:login_empleado')
def search_articulo(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre__icontains=query)|
            Q(marca__icontains=query)|
            Q(p_compra__icontains=query)|
            Q(p_venta__icontains=query)
        )
        results = Articulo.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("inventario/search_articulo.html", {
        "results": results,
        "query": query
    })

@login_required(login_url='home:login_empleado')
def search_categoria(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre__icontains=query)
        )
        results = Categoria.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("inventario/search_categoria.html", {
        "results": results,
        "query": query
    })
class ListarArticulos(LoginRequiredMixin, ListView):
    model = Articulo
    context_object_name = 'listar_articulos'
    paginate_by = 10
    template_name = 'inventario/articulos.html'

class CrearArticulo(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Articulo
    form_class = ArticuloForm
    success_message = 'El articulo %(nombre)s se ha creado correctamente'
    slug_url_kwarg = 'articulo_slug'
    template_name = 'inventario/crear_articulo.html'

class DetalleArticulo(LoginRequiredMixin, DetailView):
    model = Articulo
    template_name = 'inventario/detalle_articulo.html'
    slug_url_kwarg = 'articulo_slug'

class EditarArticulo(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Articulo
    form_class = ArticuloForm
    slug_url_kwarg = 'articulo_slug'
    success_message = 'El articulo %(nombre)s se ha editado correctamente'
    template_name = 'inventario/crear_articulo.html'

class EliminarArticulo(LoginRequiredMixin,SuccessMessageMixin,DeleteView):
    model = Articulo
    slug_url_kwarg = 'articulo_slug'
    success_url = reverse_lazy('inventario:listar_articulos')
    success_message = 'El articulo %(nombre)s eliminado correctamente'
    template_name = 'inventario/confirmar_eliminar_articulo.html'

class ListarCategorias(LoginRequiredMixin, ListView):
    model = Categoria
    paginate_by = 10
    context_object_name = 'listar_categorias'
    template_name = 'inventario/categorias.html'

class CrearCategoria(LoginRequiredMixin,SuccessMessageMixin,CreateView):
    model = Categoria
    form_class = CategoriaForm
    slug_url_kwarg = 'categoria_slug'
    success_message = 'Categoria %(nombre)s se ha creado correctamente'
    template_name = 'inventario/crear_categoria.html'

class EditarCategoria(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Categoria
    form_class = CategoriaForm
    slug_url_kwarg = 'categoria_slug'
    success_message = 'Categoria %(nombre)s  se ha editado correctamente'
    template_name = 'inventario/crear_categoria.html'

class EliminarCategoria(LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = Categoria
    slug_url_kwarg = 'categoria_slug'
    success_message = 'Categoria %(nombre)s eliminado correctamente'
    template_name = 'inventario/confirmar_eliminar_categoria.html'
    success_url = reverse_lazy('inventario:listar_categorias')
