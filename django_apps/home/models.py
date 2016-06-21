#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse


def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, filename)
    return "%s/%s" %(instance.id, filename)

class Empleado(AbstractUser):
    slug = models.SlugField(unique=True)
    INSTRUCCION = (
        ('Primaria', 'Primaria'),
        ('Secundaria', 'Secundaria'),
        ('Técnico', 'Técnico'),
        ('Superior', 'Superior'),
    )
    SEXO = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
    )
    CIVIL = (
        ('Casado', 'Casado'),
        ('Soltero', 'Soltero'),
        ('Divorciado(a)', 'Divorciado(a)'),
        ('Viudo(a)', 'Viudo(a)'),
    )
    dni = models.CharField(_('DNI'), max_length=8, null=True, blank=True)
    second_name = models.CharField(_('Second Name'), max_length=100, null=True, blank=True)
    lugar_nac = CountryField(verbose_name=_('País de Nacimiento'), null=True, blank=True)
    grado_instruc = models.CharField(_('Grado de instrucción'), choices=INSTRUCCION, max_length=10, null=True, blank=True)
    sexo = models.CharField(_('Género'), choices=SEXO, max_length=9, null=True, blank=True)
    fecha_nac = models.DateField(_('Fecha de Nacimiento'),null=True,blank=True)
    domicilio = models.CharField(_('Domicilio'), max_length=150, null=True, blank=True)
    telefono = models.CharField(_('Telefono'), max_length=9, null=True, blank=True)
    est_civil = models.CharField(_('Estado Civil'), choices=CIVIL,max_length=13, null=True, blank=True)
    avatar = models.ImageField(upload_to=upload_location, null=True, blank=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('home:detalle_empleado', kwargs={'empleado_slug':self.slug})

    class Meta(AbstractUser.Meta):
        ordering = ['-username','id']
        verbose_name_plural = 'Empleados de Only Pets'

def create_slug(instance, new_slug=None):
    slug = slugify(instance.username)
    if new_slug is not None:
        slug = new_slug
    qs = Empleado.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Empleado)
