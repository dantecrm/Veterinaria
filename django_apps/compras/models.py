#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import decimal
from django.db import models
from django_apps.core.models import TimeStampedModel
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django_apps.persona.models import Proveedor
from django_apps.inventario.models import Articulo, Categoria

@python_2_unicode_compatible
class CompraEmpresa(TimeStampedModel):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    producto = models.ForeignKey(Articulo)
    cantidad = models.IntegerField(_('Cantidad'))
    afecto = models.BooleanField(default=True)
    descuento = models.DecimalField(_('Descuento'), max_digits=16,decimal_places=2)
    val_desc = models.DecimalField(_('Valor de Descuento'), max_digits=16,decimal_places=2)
    precio_real = models.DecimalField(_('Precio Real'), max_digits=16,decimal_places=2)
    iva = models.DecimalField(_('IGV'),max_digits=16,decimal_places=2)
    total = models.DecimalField(_('Total'),max_digits=16,decimal_places=2)

    def __str__(self):
        return self.producto.nombre

    def get_absolute_url(self):
        return reverse('compras:detalle_compra', kwargs={'compra_pk':self.pk})

    def save(self,*args,**kwargs):
        if self.afecto == True:
            #Se toma en cuenta el igv
            self.precio_real = float(self.producto.p_compra) * float(self.cantidad)
            self.iva = self.precio_real * 0.18
            self.val_desc = (self.precio_real+float(self.iva)) * float(self.descuento/100)
            self.total = (self.precio_real + self.iva) - self.val_desc
        else:
            #No se toma en cuenta el igv
            self.precio_real = float(self.producto.p_compra) * float(self.cantidad)
            self.iva = 0
            self.val_desc = (self.precio_real+float(self.iva)) * float(self.descuento/100)
            self.total = (self.precio_real + self.iva) - self.val_desc
        super(CompraEmpresa,self).save(*args,**kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Compras de la Empresa'
