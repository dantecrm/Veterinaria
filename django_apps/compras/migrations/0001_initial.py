# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 02:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventario', '0001_initial'),
        ('persona', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompraEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('cantidad', models.IntegerField(verbose_name='Cantidad')),
                ('afecto', models.BooleanField(default=True)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Descuento')),
                ('val_desc', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Valor de Descuento')),
                ('precio_real', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Precio Real')),
                ('iva', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='IGV')),
                ('total', models.DecimalField(decimal_places=2, max_digits=16, verbose_name='Total')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Categoria')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Articulo')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persona.Proveedor')),
            ],
            options={
                'ordering': ['-id'],
                'verbose_name_plural': 'Compras de la Empresa',
            },
        ),
    ]
