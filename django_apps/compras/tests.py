# -*- coding: utf-8 -*-
import tempfile
from django.test import TestCase, Client
from .models import CompraEmpresa
from django_apps.home.models import Empleado
from django_apps.inventario.models import Articulo, Categoria
from django_apps.persona.models import Proveedor
from django.core.urlresolvers import reverse

def create_proveedor(razon_social,ruc,descripcion,direccion,contacto,email):
    image = tempfile.NamedTemporaryFile(suffix='.jpg').name
    return Proveedor.objects.create(razon_social=razon_social,ruc=ruc,
                                    descripcion=descripcion,direccion=direccion,
                                    contacto=contacto,email=email,avatar=image)

def create_categoria(nombre):
    return Categoria.objects.create(nombre=nombre)

def create_producto(nombre,marca,p_compra,p_venta):
    image = tempfile.NamedTemporaryFile(suffix='.jpg').name
    return Articulo.objects.create(nombre = nombre, marca = marca, p_compra=p_compra,
                                   p_venta = p_venta, avatar = image)

def create_compra(proveedor,categoria,producto,cantidad,descuento):
    return CompraEmpresa.objects.create(proveedor_id=proveedor,categoria_id=categoria,producto_id=producto,cantidad=cantidad,descuento=descuento)

class OrdenCompraViewTests(TestCase):
    def setUp(self):
        Empleado.objects.create_user('admin','admin@gmail.com','dante2016')
        self.client.login(username='admin',password='dante2016')

    def test_create_ordencompra(self):
        proveedor = create_proveedor(razon_social='Only Pets', ruc='23781942711',
                                     descripcion='Esta empresa es una veterinaria', direccion='Jr. Junin # 328',
                                     contacto='Hector Caira Mamani',email='veterinariaonlypetscanissur@gmail.com')
        categoria = create_categoria(nombre='Alimentacion')
        producto = create_producto(nombre='Croquetas de Maiz',marca='RicoCan',p_compra=30,p_venta=40)
        compra = create_compra(proveedor=proveedor.id,categoria=categoria.id,producto=producto.id,cantidad=60,descuento=10.00)
        self.assertEqual(compra.pk, 1)
        # response = self.client.get('compras:listar_compras',follow=True)
        # print(response)
        # self.assertQuerysetEqual(response.context['listar_compras'], ['<CompraEmpresa: Croquetas de Maiz>'])

    def test_detail_ordencompra(self):
        proveedor = create_proveedor(razon_social='Only Pets', ruc='23781942711',
                                     descripcion='Esta empresa es una veterinaria', direccion='Jr. Junin # 328',
                                     contacto='Hector Caira Mamani',email='veterinariaonlypetscanissur@gmail.com')
        categoria = create_categoria(nombre='Alimentacion')
        producto = create_producto(nombre='Croquetas de Maiz',marca='RicoCan',p_compra=30,p_venta=40)
        compra = create_compra(proveedor=proveedor.id,categoria=categoria.id,producto=producto.id,cantidad=60,descuento=10.00)
        # print(compra.id)
        url = reverse('compras:detalle_compra',args=(compra.id,))
        response = self.client.get(url,follow=True)
        self.assertEqual(200,response.status_code)

    def test_delete_ordencompra(self):
        c = Client()
        proveedor = create_proveedor(razon_social='Only Pets', ruc='23781942711',
                                     descripcion='Esta empresa es una veterinaria', direccion='Jr. Junin # 328',
                                     contacto='Hector Caira Mamani',email='veterinariaonlypetscanissur@gmail.com')
        categoria = create_categoria(nombre='Alimentacion')
        producto = create_producto(nombre='Croquetas de Maiz',marca='RicoCan',p_compra=30,p_venta=40)
        compra = create_compra(proveedor=proveedor.id,categoria=categoria.id,producto=producto.id,cantidad=60,descuento=10.00)
        url = reverse('compras:eliminar_compra',args=(compra.id,))
        response =self.client.get(url,follow=True,secure=True)
        # print(response)
        self.assertEqual(200,response.status_code)
