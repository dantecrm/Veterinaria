#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django.test import TestCase, Client
import tempfile
from .models import Articulo, Categoria
from django_apps.home.models import Empleado
from django.core.urlresolvers import reverse

def create_articulo(nombre, marca,p_compra,p_venta):
    image = tempfile.NamedTemporaryFile(suffix='.jpg').name
    return Articulo.objects.create(nombre = nombre, marca = marca, p_compra=p_compra,
                                   p_venta = p_venta, avatar = image)

class ArticuloViewTests(TestCase):
    def setUp(self):
        user = Empleado.objects.create_user('admin','admin@gmail.com','dante2016')
        self.client.login(username='admin',password='dante2016')

    def test_status_article(self):
        response = self.client.get(reverse('inventario:listar_articulos'), follow=True)
        user = Empleado.objects.get(username='admin')
        self.assertEqual(response.status_code, 200)

    def test_create_article(self):
        create_articulo(nombre='Comida de Mascota',marca='RicoCan',p_compra=20,p_venta=30)
        response = self.client.get(reverse('inventario:listar_articulos'),follow=True)
        self.assertQuerysetEqual(response.context['listar_articulos'], ['<Articulo: Comida de Mascota>'])

    def test_detalle_articulo(self):
        c = Client()
        a = create_articulo(nombre='Comida de Mascota',marca='RicoCan',p_compra=20,p_venta=30)
        url = reverse('inventario:detalle_articulo',args=(a.id,))
        # c.login(username='admin',password='dante2016')
        response = c.get(url,follow=True)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, a.nombre)

    def test_delete_articulo(self):
        c = Client()
        a = create_articulo(nombre='Comida de Mascota',marca='RicoCan',p_compra=20,p_venta=30)
        url = reverse('inventario:eliminar_articulo',args=(a.id,))
        response = c.delete(url,follow=True)
        self.assertEqual(200,response.status_code)

def create_categoria(nombre):
    return Categoria.objects.create(nombre=nombre)

class CategoriaViewTests(TestCase):
    def setUp(self):
        user = Empleado.objects.create_user('admin','admin@gmail.com','dante2016')
        self.client.login(username='admin',password='dante2016')

    def test_status_categoria(self):
        response = self.client.get(reverse('inventario:listar_categorias'), follow=True)
        user = Empleado.objects.get(username='admin')
        self.assertEqual(response.status_code, 200)

    def test_create_categoria(self):
        create_categoria(nombre='Accesorios')
        response = self.client.get(reverse('inventario:listar_categorias'),follow=True)
        self.assertQuerysetEqual(response.context['listar_categorias'], ['<Categoria: Accesorios>'])

    def test_delete_categoria(self):
        c = Client()
        a = create_categoria(nombre='Alimento')
        url = reverse('inventario:eliminar_categoria',args=(a.id,))
        response = c.delete(url,follow=True)
        self.assertEqual(200,response.status_code)
