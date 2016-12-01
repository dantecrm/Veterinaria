#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from django.test import TestCase, Client
# import tempfile
# from .models import Mascota, Vacuna, Desparacitante, EstadoMascota
# from django_apps.home.models import Empleado
# from django_apps.persona.models import Cliente
# from django.core.urlresolvers import reverse

# def create_mascota(propietario, nombre, raza, color, especie, edad, peso, descripcion, avatar,
#                    ambiental, alimento, bano):
#     image = tempfile.NamedTemporaryFile(suffix='.jpg').name
#     return Mascota.objects.create(propietario=propietario,nombre=nombre,raza=raza,
#                                   color=color,especie=especie,edad=edad,peso=peso,
#                                   descripcion=descripcion,avatar=image,ambiental=ambiental,
#                                   alimento=alimento,bano=bano)

# def create_cliente(nombre,ap_pater,ap_mater,dni,sexo,domicilio,telefono):
#     image = tempfile.NamedTemporaryFile(suffix='.jpg').name
#     return Cliente.objects.create(nombre=nombre,ap_pater=ap_pater,ap_mater=ap_mater,
#                                   dni=dni,sexo=sexo,domicilio=domicilio,telefono=telefono,avatar=image)

# def create_vacuna(mascota,vacuna,fecha):
#     return Vacuna.objects.create(mascota=mascota,vacuna=vacuna,fecha=fecha)

# def create_desparacitante(mascota,producto,fecha):
#     return Desparacitante.objects.create(mascota=mascota,producto=producto,fecha=fecha)

# def create_estadomascota(mascota,motivo,fr,fp,fc,t,exampiel,examucvis,gangpal,apetito,sed,defecac,miccion):
#     return EstadoMascota.objects.create(mascota=mascota,motivo=motivo,fr=fr,fp=fp,fc=fc,t=t,
#                                         exampiel=exampiel,examucvis=examucvis,gangpal=gangpal,apetito=apetito,sed=sed,
#                                         defecac=defecac,miccion=miccion)

# class MascotaViewTests(TestCase):
#     def setUp(self):
#         user = Empleado.objects.create_user('admin','admin@gmail.com','dante2016')
#         self.client.login(username='admin',password='dante2016')

#     def test_status_mascota(self):
#         response = self.client.get(reverse('clinica:listar_mascotas'), follow=True)
#         user = Empleado.objects.get(username='admin')
#         self.assertEqual(response.status_code, 200)

#     def test_create_mascota(self):
#         cliente = create_cliente(nombre='Thomas',ap_pater='Alva',ap_mater='Edison',
#                                  dni='38163749',sexo='Masculino',domicilio='Av. Circunvalación N° 1303',
#                                  telefono='952214712')
#         create_mascota(propietario=cliente.id,nombre='Peluchin',raza='Cobrador Dorado',
#                        color='Amarillo Dorado',especie='Canino',edad=4.00,peso=15.00,
#                        descripcion='Esta mascota es de tamaño promedio',ambiental='Desde hace una semana',
#                        alimento='Comida Casera',bano='4 veces a al mes')
        # response = self.client.get(reverse('clinica:listar_mascotas'),follow=True)
        # self.assertQuerysetEqual(response.context['listar_mascotas'], ['<Mascota: Thomas:Peluchin <=> 0001-00001'])

    # def test_detalle_articulo(self):
    #     c = Client()
    #     a = create_articulo(nombre='Comida de Mascota',marca='RicoCan',p_compra=20,p_venta=30)
    #     url = reverse('inventario:detalle_articulo',args=(a.id,))
    #     # c.login(username='admin',password='dante2016')
    #     response = c.get(url,follow=True)
    #     self.assertEqual(response.status_code, 200)
    #     # self.assertContains(response, a.nombre)

    # def test_delete_articulo(self):
    #     c = Client()
    #     a = create_articulo(nombre='Comida de Mascota',marca='RicoCan',p_compra=20,p_venta=30)
    #     url = reverse('inventario:eliminar_articulo',args=(a.id,))
    #     response = c.delete(url,follow=True)
    #     self.assertEqual(200,response.status_code)

# def create_categoria(nombre):
#     return Categoria.objects.create(nombre=nombre)

# class CategoriaViewTests(TestCase):
#     def setUp(self):
#         user = Empleado.objects.create_user('admin','admin@gmail.com','dante2016')
#         self.client.login(username='admin',password='dante2016')

#     def test_status_categoria(self):
#         response = self.client.get(reverse('inventario:listar_categorias'), follow=True)
#         user = Empleado.objects.get(username='admin')
#         self.assertEqual(response.status_code, 200)

#     def test_create_categoria(self):
#         create_categoria(nombre='Accesorios')
#         response = self.client.get(reverse('inventario:listar_categorias'),follow=True)
#         self.assertQuerysetEqual(response.context['listar_categorias'], ['<Categoria: Accesorios>'])

#     def test_delete_categoria(self):
#         c = Client()
#         a = create_categoria(nombre='Alimento')
#         url = reverse('inventario:eliminar_categoria',args=(a.id,))
#         response = c.delete(url,follow=True)
#         self.assertEqual(200,response.status_code)
