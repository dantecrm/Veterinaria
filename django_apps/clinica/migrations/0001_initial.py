# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 02:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_apps.clinica.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desparacitante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.CharField(max_length=150, verbose_name='Producto')),
                ('fecha', models.DateField(verbose_name='Fecha')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoMascota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('motivo', models.CharField(max_length=200, verbose_name='Motivo')),
                ('fichaseg', models.CharField(editable=False, max_length=13, verbose_name='N\xb0 de ficha de seguimiento')),
                ('slug', models.SlugField(unique=True)),
                ('fr', models.CharField(max_length=50, verbose_name='FR')),
                ('fc', models.CharField(max_length=50, verbose_name='FC')),
                ('fp', models.CharField(max_length=50, verbose_name='FP')),
                ('t', models.CharField(max_length=50, verbose_name='T')),
                ('exampiel', models.CharField(max_length=400, verbose_name='Examen de piel')),
                ('examucvis', models.CharField(max_length=400, verbose_name='Examen de mucosas visibles')),
                ('gangpal', models.CharField(max_length=400, verbose_name='Ganglios palpables')),
                ('apetito', models.CharField(max_length=200, verbose_name='Apetito')),
                ('sed', models.CharField(max_length=200, verbose_name='Sed')),
                ('defecac', models.CharField(max_length=200, verbose_name='Defecaci\xf3n')),
                ('miccion', models.CharField(max_length=200, verbose_name='Miccion')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'Estados de los pacientes',
            },
        ),
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('ficha', models.CharField(editable=False, max_length=5, verbose_name='Ficha')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre')),
                ('slug', models.SlugField(unique=True)),
                ('raza', models.CharField(max_length=100, verbose_name='Raza')),
                ('color', models.CharField(max_length=100, verbose_name='Color')),
                ('especie', models.CharField(max_length=100, verbose_name='Especie')),
                ('edad', models.PositiveSmallIntegerField(verbose_name='Edad')),
                ('peso', models.PositiveSmallIntegerField(verbose_name='Peso')),
                ('descripcion', models.TextField(verbose_name='Descripcion')),
                ('avatar', models.ImageField(upload_to=django_apps.clinica.models.upload_location)),
                ('ambiental', models.TextField(help_text='\xbfDesde cuando est\xe1 enfermo el animal?, \xbfSi esta enfermedad ha sido tratada o no?', verbose_name='Ambiental')),
                ('alimento', models.TextField(help_text='\xbf Qu\xe9 tipo de dieta se le suministra? Casera o fabricado (seca, h\xfameda,semi seca)', verbose_name='Alimento')),
                ('bano', models.TextField(help_text='\xbfCuantas veces por mes se le ba\xf1a al animal?', verbose_name='Ba\xf1o')),
                ('propietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.Cliente', verbose_name='Propietario')),
            ],
            options={
                'ordering': ['-id', '-nombre'],
                'verbose_name_plural': 'Mascotas',
            },
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vacuna', models.CharField(max_length=150, verbose_name='Vacuna')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.Mascota')),
            ],
        ),
        migrations.AddField(
            model_name='estadomascota',
            name='mascota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.Mascota'),
        ),
        migrations.AddField(
            model_name='desparacitante',
            name='mascota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinica.Mascota'),
        ),
    ]
