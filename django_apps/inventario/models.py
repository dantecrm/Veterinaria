#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_apps.core.models import TimeStampedModel
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django_countries.fields import CountryField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, filename)
    return "%s/%s" %(instance.id, filename)

@python_2_unicode_compatible
class Articulo(TimeStampedModel):
    codigo = models.CharField(_('Código'), max_length=13, editable=False)
    nombre = models.CharField(_('Nombre'), max_length=100)
    slug = models.SlugField(unique=True)
    marca = models.CharField(_('Marca'), max_length=100)
    p_compra = models.DecimalField(_('Precio de Compra'), max_digits=4, decimal_places=2)
    p_venta = models.DecimalField(_('Precio de Venta'), max_digits=4, decimal_places=2)
    avatar = models.ImageField(upload_to=upload_location)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('inventario:detalle_articulo', kwargs={'articulo_slug':self.slug})

    def save(self, *args, **kwargs):
        #Hallando el dígito verificador
        a = '7752016'
        i = Articulo.objects.count()
        if i==None:
            b = 1
        else:
            b = i+1
        b = '{0:05}'.format(b)
        s = a + b
        dv = a + b
        s = " ".join(s)
        s = s.split(" ")
        n = [int(s[i]) for i in range(len(s)) if i%2!=0]
        n = sum(n)
        n = n * 3
        m = [int(s[i]) for i in range(len(s)) if i%2==0]
        m= sum(m)
        x = n + m
        if x % 10 == 0:
            res = 0
            self.codigo = '{0}{1}'.format(dv,res)
        else:
            r = (x + 9) - ((x + 9)%10)
            res = r - x
            self.codigo = '{0}{1}'.format(dv,res)
        super(Articulo, self).save(*args,**kwargs)

    class Meta:
        ordering = ['-nombre']
        verbose_name_plural = 'Articulos'

def create_slug_articulo(instance, new_slug=None):
    slug = slugify(instance.nombre)
    if new_slug is not None:
        slug = new_slug
    qs = Articulo.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_articulo(instance, new_slug=new_slug)
    return slug

def pre_save_articulo_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_articulo(instance)

pre_save.connect(pre_save_articulo_receiver, sender=Articulo)

class Categoria(models.Model):
    nombre = models.CharField(_('Categoría'), max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('inventario:listar_categorias')

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Categorías'

def create_slug_categoria(instance, new_slug=None):
    slug = slugify(instance.nombre)
    if new_slug is not None:
        slug = new_slug
    qs = Categoria.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_categoria(instance, new_slug=new_slug)
    return slug

def pre_save_categoria_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_categoria(instance)

pre_save.connect(pre_save_categoria_receiver, sender=Categoria)
