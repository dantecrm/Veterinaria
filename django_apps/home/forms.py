#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.forms import UserChangeForm
from .models import Empleado


class EmpleadoEditForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Empleado
        fields = ['username','password','email','is_staff','first_name','last_name',
                  'second_name','dni','lugar_nac', 'grado_instruc','sexo','fecha_nac','domicilio','telefono',
                  'est_civil','avatar']
    def __init__(self, *args, **kwargs):
        super(EmpleadoEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class' : 'form-control','placeholder':'Nombre de Usuario'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control','placeholder':'Correo Eletrónico'})
        self.fields['first_name'].widget.attrs.update({'class' : 'form-control','placeholder':'Nombres'})
        self.fields['last_name'].widget.attrs.update({'class' : 'form-control','placeholder':'Apellido Paterno'})
        self.fields['second_name'].widget.attrs.update({'class' : 'form-control','placeholder':'Apellido Materno'})
        self.fields['dni'].widget.attrs.update({'class' : 'form-control','placeholder':'DNI'})
        self.fields['lugar_nac'].widget.attrs.update({'class' : 'chosen'})
        self.fields['grado_instruc'].widget.attrs.update({'class' : 'chosen'})
        self.fields['sexo'].widget.attrs.update({'class' : 'chosen'})
        self.fields['est_civil'].widget.attrs.update({'class' : 'chosen'})
        self.fields['fecha_nac'].widget.attrs.update({'class' : 'form-control date-picker'})
        self.fields['domicilio'].widget.attrs.update({'class' : 'form-control','placeholder':'Domicilio'})
        self.fields['telefono'].widget.attrs.update({'class' : 'form-control','placeholder':'Teléfono'})

class CrearEmpleadoForm(ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label=" Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label=" Confirm Password")
    #Esta función clean_password(self) verifica que las contraseñas sean iguales
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2  and password1 != password2:
            raise forms.ValidationError("Los Passwords no son iguales")
        password_validation.validate_password(self.cleaned_data.get('password2'), self.instance)
        return password2

    def save(self, commit=True):
        empleado = super(CreateUserForm, self).save(commit=False)
        empleado.set_password(self.cleaned_data["password1"])
        if commit:
            empleado.save()
        return empleado

    class Meta:
        model = Empleado
        fields = ('username','email')
