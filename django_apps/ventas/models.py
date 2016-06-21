#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_apps.core.models import TimeStampedModel
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils import timezone

from django_apps.persona.models import Cliente
from django_apps.compras.models import CompraEmpresa

@python_2_unicode_compatible
class OrdenVenta(TimeStampedModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    codigo = models.CharField(_('Código'), max_length=12, editable=False)

    def __str__(self):
        return "{0}:{1}".format(self.cliente.nombre,self.codigo)

    def get_absolute_url(self):
        return reverse('ventas:detalle_venta', kwargs={'venta_pk':self.pk})

    def save(self, *args, **kwargs):
        a = timezone.now().year
        b = timezone.now().month
        c = OrdenVenta.objects.count()
        if c == None:
            n = 1
        else:
            n = c + 1
        self.codigo = "{0}-{1:02}-{2:04}".format(a,b,n)
        super(OrdenVenta,self).save(*args,**kwargs)

@python_2_unicode_compatible
class CarritoVenta(models.Model):
    venta = models.ForeignKey(OrdenVenta, on_delete=models.CASCADE)
    producto = models.ForeignKey(CompraEmpresa, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(_('Cantidad'))
    precio_real = models.DecimalField(_('Precio Real'),max_digits=16,decimal_places=2)
    iva = models.DecimalField(_('IGV'),max_digits=16,decimal_places=2)
    total = models.DecimalField(_('Total'),max_digits=16,decimal_places=2)

    def __str__(self):
        return "%s: %s" %(self.venta.cliente.nombre,self.producto.producto.nombre)

    def save(self,*args,**kwargs):
        self.precio_real = float(self.producto.producto.p_venta) * float(self.cantidad)
        self.iva = self.precio_real * 0.18
        self.total = self.precio_real + self.iva
        super(CarritoVenta, self).save(*args,**kwargs)

@receiver(post_save, sender=CarritoVenta, dispatch_uid="Actualizar_stock_count")
def update_stock(sender, instance, **kwargs):
     instance.producto.cantidad -= instance.cantidad
     instance.producto.save()
