#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from django import forms
from .models import Cliente, Proveedor

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre','ap_pater','ap_mater','dni','sexo','domicilio','telefono','avatar']

    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
        self.fields['ap_pater'].widget.attrs.update({'class' : 'form-control'})
        self.fields['ap_mater'].widget.attrs.update({'class' : 'form-control'})
        self.fields['dni'].widget.attrs.update({'class' : 'form-control'})
        self.fields['sexo'].widget.attrs.update({'class' : 'chosen'})
        self.fields['domicilio'].widget.attrs.update({'class' : 'form-control'})
        self.fields['telefono'].widget.attrs.update({'class' : 'form-control'})

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['razon_social','ruc','descripcion','direccion','contacto','email','avatar']

    def __init__(self, *args, **kwargs):
        super(ProveedorForm, self).__init__(*args, **kwargs)
        self.fields['razon_social'].widget.attrs.update({'class' : 'form-control'})
        self.fields['ruc'].widget.attrs.update({'class' : 'form-control'})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control','rows':'4','placeholder':'Breve descripción de la Empresa'})
        self.fields['direccion'].widget.attrs.update({'class' : 'form-control'})
        self.fields['contacto'].widget.attrs.update({'class' : 'form-control'})
        self.fields['direccion'].widget.attrs.update({'class' : 'form-control'})
        self.fields['email'].widget.attrs.update({'class' : 'form-control'})

