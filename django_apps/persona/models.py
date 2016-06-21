#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.template import defaultfilters
from django_countries.fields import CountryField
from django_apps.core.models import TimeStampedModel
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse

def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, filename)
    return "%s/%s" %(instance.id, filename)

class Cliente(TimeStampedModel):
    SEXO = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    )
    nombre = models.CharField(_('Nombre'), max_length=100)
    slug = models.SlugField(unique=True)
    ap_pater = models.CharField(_('Apellido Paterno'), max_length=100)
    ap_mater = models.CharField(_('Apellido Materno'), max_length=100)
    dni = models.CharField(_('DNI'), max_length=8)
    sexo = models.CharField(_('Género'), choices=SEXO, max_length=9)
    domicilio = models.CharField(('Domicilio'), max_length=150)
    telefono = models.CharField(('Teléfono'), max_length=9)
    avatar = models.ImageField(upload_to=upload_location)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('persona:detalle_cliente', kwargs={'cliente_slug':self.slug})

    # def save(self, *args, **kwargs):
    #     a = self.nombre
    #     a = a.lower()
    #     if not self.id:
    #         self.slug = defaultfilters.slugify(a)
    #         super(Cliente, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Clientes'

def create_slug_cliente(instance, new_slug=None):
    slug = slugify(instance.nombre)
    if new_slug is not None:
        slug = new_slug
    qs = Cliente.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_cliente(instance, new_slug=new_slug)
    return slug

def pre_save_cliente_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_cliente(instance)

pre_save.connect(pre_save_cliente_receiver, sender=Cliente)

class Proveedor(TimeStampedModel):
    razon_social = models.CharField(_('Razón Social'), max_length=150)
    ruc = models.CharField(_('RUC'), max_length=11)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField(_('Descripción'))
    direccion = models.CharField(_('Dirección'), max_length=150)
    contacto = models.CharField(_('Contacto'), max_length=150)
    email = models.EmailField(_('Correo Electrónico'))
    avatar = models.ImageField(upload_to=upload_location)

    def __unicode__(self):
        return self.razon_social

    def __str__(self):
        return self.razon_social

    def get_absolute_url(self):
        return reverse('persona:detalle_proveedor', kwargs={'proveedor_slug':self.slug})

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Proveedores'

def create_slug_proveedor(instance, new_slug=None):
    slug = slugify(instance.razon_social)
    if new_slug is not None:
        slug = new_slug
    qs = Proveedor.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_proveedor(instance, new_slug=new_slug)
    return slug

def pre_save_proveedor_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_proveedor(instance)

pre_save.connect(pre_save_proveedor_receiver, sender=Proveedor)
