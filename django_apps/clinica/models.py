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
from django_apps.persona.models import Cliente

def upload_location(instance, filename):
    # filebase, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, filename)
    return "%s/%s" %(instance.id, filename)

@python_2_unicode_compatible
class Mascota(TimeStampedModel):
    propietario = models.ForeignKey(Cliente, verbose_name=_('Propietario'), on_delete=models.CASCADE)
    ficha = models.CharField(_('Ficha'), max_length=5, editable=False)
    nombre = models.CharField(_('Nombre'), max_length=100)
    slug = models.SlugField(unique=True)
    raza = models.CharField(_('Raza'), max_length=100)
    color = models.CharField(_('Color'), max_length=100)
    especie = models.CharField(_('Especie'), max_length=100)
    edad = models.PositiveSmallIntegerField(_('Edad'))
    peso = models.PositiveSmallIntegerField(_('Peso'))
    descripcion = models.TextField(_('Descripcion'))
    avatar = models.ImageField(upload_to=upload_location)
    # Anamnesis
    ambiental = models.TextField(_('Ambiental'), help_text=_('¿Desde cuando está enfermo el animal?, ¿Si esta enfermedad ha sido tratada o no?'))
    alimento = models.TextField(_('Alimento'), help_text=_('¿ Qué tipo de dieta se le suministra? Casera o fabricado (seca, húmeda,semi seca)'))
    bano = models.TextField(_('Baño'), help_text=_('¿Cuantas veces por mes se le baña al animal?'))

    def __str__(self):
        return "{0}:{1} <=> {2}".format(self.propietario.nombre, self.nombre,self.ficha)

    def get_absolute_url(self):
        return reverse('clinica:detalle_mascota', kwargs={'cliente_slug':self.propietario.slug,'mascota_slug':self.slug})

    def save(self, *args, **kwargs):
        mascotas = Mascota.objects.count()
        if mascotas == None:
            num = 1
        else:
            num = mascotas + 1
        self.ficha = "{0:04}-{0:05}".format(self.propietario.id,num)
        super(Mascota,self).save(*args,**kwargs)

    class Meta:
        ordering = ['-id','-nombre']
        verbose_name_plural = 'Mascotas'

def create_slug_mascota(instance, new_slug=None):
    slug = slugify(instance.nombre)
    if new_slug is not None:
        slug = new_slug
    qs = Mascota.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_mascota(instance, new_slug=new_slug)
    return slug

def pre_save_mascota_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_mascota(instance)

pre_save.connect(pre_save_mascota_receiver, sender=Mascota)

class Vacuna(models.Model):
    mascota = models.ForeignKey(Mascota,on_delete=models.CASCADE)
    vacuna = models.CharField(_('Vacuna'), max_length=150)
    fecha = models.DateField(_('Fecha'))

    def __str__(self):
        return self.vacuna

class Desparacitante(models.Model):
    mascota = models.ForeignKey(Mascota,on_delete=models.CASCADE)
    producto = models.CharField(_('Producto'), max_length=150)
    fecha = models.DateField(_('Fecha'))

    def __str__(self):
        return self.producto

@python_2_unicode_compatible
class EstadoMascota(TimeStampedModel):
    mascota = models.ForeignKey(Mascota,on_delete=models.CASCADE)
    motivo = models.CharField(_('Motivo'), max_length=200)
    fichaseg = models.CharField(_('N° de ficha de seguimiento'), max_length=13, editable=False)
    slug = models.SlugField(unique=True)
    #CONSTANTES CLÍNICAS
    fr = models.CharField(_('FR'), max_length=50)
    fc = models.CharField(_('FC'), max_length=50)
    fp = models.CharField(_('FP'), max_length=50)
    t = models.CharField(_('T'), max_length=50)
    #OTROS
    exampiel = models.CharField(_('Examen de piel'), max_length=400)
    examucvis = models.CharField(_('Examen de mucosas visibles'), max_length=400)
    gangpal = models.CharField(_('Ganglios palpables'), max_length=400)
    #GRANDES FUNCIONES ORGáNICAS
    apetito = models.CharField(_('Apetito'), max_length=200)
    sed = models.CharField(_('Sed'), max_length=200)
    defecac = models.CharField(_('Defecación'), max_length=200)
    miccion = models.CharField(_('Miccion'), max_length=200)

    def __str__(self):
        return "Seguimiento de la {0}".format(self.mascota.nombre)

    def get_absolute_url(self):
        return reverse('clinica:detalle_estado_mascota', kwargs={'cliente_slug':self.mascota.propietario.slug,'mascota_slug':self.mascota.slug,'estado_slug':self.slug})

    def save(self,*args,**kwargs):
        estmasc = EstadoMascota.objects.count()
        if estmasc == None:
            num = 1
        else:
            num = estmasc + 1
        self.fichaseg="{0}-{1:03}".format(self.mascota.ficha,num)
        super(EstadoMascota,self).save(*args,**kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = 'Estados de los pacientes'

def create_slug_estado(instance, new_slug=None):
    slug = slugify(instance.fichaseg)
    if new_slug is not None:
        slug = new_slug
    qs = EstadoMascota.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug_estado(instance, new_slug=new_slug)
    return slug

def pre_save_estado_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug_estado(instance)

pre_save.connect(pre_save_estado_receiver, sender=EstadoMascota)
