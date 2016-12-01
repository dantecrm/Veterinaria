import tempfile
from django.test import TestCase, Client
from .models import Cliente, Proveedor
from django.core.urlresolvers import reverse
from django_apps.home.models import Empleado

def create_cliente(nombre, ap_pater, ap_mater,dni,sexo,domicilio,telefono):
    image = tempfile.NamedTemporaryFile(suffix='.jpg').name
    return Cliente.objects.create(nombre = nombre, ap_pater = ap_pater, ap_mater=ap_mater,
                                   dni = dni, sexo = sexo, domicilio = domicilio, telefono = telefono, avatar = image)

class ClienteViewTests(TestCase):
    def setUp(self):
        user = Empleado.objects.create_user('wilber','admin@gmail.com','123456qwe')
        self.client.login(username='wilber',password='123456qwe')

    def test_status_cliente(self):
        response = self.client.get(reverse('persona:listar_clientes'), follow=True)
        user = Empleado.objects.get(username='wilber')
        self.assertEqual(response.status_code, 200)

    def test_create_cliente(self):
        create_cliente(nombre='wilber',ap_pater='choque',ap_mater='quenta',dni=12345678,sexo='Masculino',domicilio='aqp',telefono=123456789)
        response = self.client.get(reverse('persona:listar_clientes'),follow=True)
        self.assertQuerysetEqual(response.context['listar_clientes'], ['<Cliente: wilber>'])

    def test_detalle_cliente(self):
        c = Client()
        a = create_cliente(nombre='wilber',ap_pater='choque',ap_mater='quenta',dni=12345678,sexo='Masculino',domicilio='aqp',telefono=123456789)
        url = reverse('persona:detalle_cliente',args=(a.id,))
        # c.login(username='admin',password='dante2016')
        response = c.get(url,follow=True)
        self.assertEqual(response.status_code, 200)

    def test_delete_cliente(self):
        c = Client()
        a = create_cliente(nombre='wilber',ap_pater='choque',ap_mater='quenta',dni=12345678,sexo='Masculino',domicilio='aqp',telefono=123456789)

        url = reverse('persona:eliminar_cliente',args=(a.id,))
        # c.login(username='admin',password='dante2016')
        #response = c.get(url,follow=True,secure=True)
        #self.assertEqual(response.status_code, 200)


def create_proveedor(razon_social, ruc, descripcion,direccion,contacto,email):
    image = tempfile.NamedTemporaryFile(suffix='.jpg').name
    return Cliente.objects.create(razon_social = razon_social, ruc= ruc, descripcion=descripcion,
                                   direccion = direccion, contacto = contacto, email = email, avatar=image)

class ProveedorViewTests(TestCase):
    def setUp(self):
        user = Empleado.objects.create_user('wilber','admin@gmail.com','123456qwe')
        self.client.login(username='wilber',password='123456qwe')

    def test_status_proveedor(self):
        response = self.client.get(reverse('persona:listar_proveedores'), follow=True)
        user = Empleado.objects.get(username='wilber')
        self.assertEqual(response.status_code, 200)

