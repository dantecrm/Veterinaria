# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-21 02:34
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import django_apps.home.models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('slug', models.SlugField(unique=True)),
                ('dni', models.CharField(blank=True, max_length=8, null=True, verbose_name='DNI')),
                ('second_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Second Name')),
                ('lugar_nac', django_countries.fields.CountryField(blank=True, max_length=2, null=True, verbose_name='Pa\xeds de Nacimiento')),
                ('grado_instruc', models.CharField(blank=True, choices=[('Primaria', 'Primaria'), ('Secundaria', 'Secundaria'), ('T\xe9cnico', 'T\xe9cnico'), ('Superior', 'Superior')], max_length=10, null=True, verbose_name='Grado de instrucci\xf3n')),
                ('sexo', models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], max_length=9, null=True, verbose_name='G\xe9nero')),
                ('fecha_nac', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('domicilio', models.CharField(blank=True, max_length=150, null=True, verbose_name='Domicilio')),
                ('telefono', models.CharField(blank=True, max_length=9, null=True, verbose_name='Telefono')),
                ('est_civil', models.CharField(blank=True, choices=[('Casado', 'Casado'), ('Soltero', 'Soltero'), ('Divorciado(a)', 'Divorciado(a)'), ('Viudo(a)', 'Viudo(a)')], max_length=13, null=True, verbose_name='Estado Civil')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=django_apps.home.models.upload_location)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-username', 'id'],
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'Empleados de Only Pets',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
