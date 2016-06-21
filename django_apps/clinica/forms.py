# -*- coding: utf-8 -*-
from django import forms
from django_apps.persona.models import Cliente
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from .models import Mascota, Vacuna, Desparacitante, EstadoMascota

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['propietario','nombre','raza','color','especie','edad',
                  'peso','descripcion','avatar','ambiental','alimento','bano']

    def __init__(self, *args, **kwargs):
        super(MascotaForm, self).__init__(*args, **kwargs)
        self.fields['propietario'].widget.attrs.update({'class' : 'chosen'})
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
        self.fields['raza'].widget.attrs.update({'class' : 'form-control'})
        self.fields['color'].widget.attrs.update({'class' : 'form-control'})
        self.fields['especie'].widget.attrs.update({'class' : 'form-control'})
        self.fields['edad'].widget.attrs.update({'class' : 'form-control input-mask','placeholder':'eg: 000.000.000.000.000,00'})
        self.fields['peso'].widget.attrs.update({'class' : 'form-control input-mask','placeholder':'eg: 000.000.000.000.000,00'})
        self.fields['descripcion'].widget.attrs.update({'class' : 'form-control','rows':'4','placeholder':'Breve descripción de la Mascota'})
        self.fields['ambiental'].widget.attrs.update({'class' : 'form-control','rows':'4','placeholder':'¿Desde cuando está enfermo el animal?\n¿Si esta enfermedad ha sido tratada o no?'})
        self.fields['alimento'].widget.attrs.update({'class' : 'form-control','rows':'6','placeholder':'¿Qué tipo de dieta se le suministra?\nCasera o fabricado (seca, húmeda,semi seca)\nMarca de la comida,\nTipo de alimentación(libre elección o comida individual)'})
        self.fields['bano'].widget.attrs.update({'class' : 'form-control','rows':'4','placeholder':'¿Cuantas veces por mes se le baña al animal?'})

class VacunaForm(forms.ModelForm):
    class Meta:
        model = Vacuna
        fields = ['vacuna','fecha']

    def __init__(self, *args, **kwargs):
        super(VacunaForm, self).__init__(*args, **kwargs)
        self.fields['vacuna'].widget.attrs.update({'class' : 'form-control vacuna'})
        self.fields['fecha'].widget.attrs.update({'class' : 'form-control input-mask','data-mask':'00/00/0000','placeholder':'eg: 23/05/2014','maxlength':'10','autocomplete':'off'})

class DesparacitanteForm(forms.ModelForm):
    class Meta:
        model = Desparacitante
        fields = ['producto','fecha']

    def __init__(self, *args, **kwargs):
        super(DesparacitanteForm, self).__init__(*args, **kwargs)
        self.fields['producto'].widget.attrs.update({'class' : 'form-control despar'})
        self.fields['fecha'].widget.attrs.update({'class' : 'form-control input-mask','data-mask':'00/00/0000','placeholder':'eg: 23/05/2014','maxlength':'10','autocomplete':'off'})

class EstadoMascotaForm(forms.ModelForm):
    class Meta:
        model = EstadoMascota
        fields = ['mascota','motivo','fr','fc','fp','t','exampiel','examucvis',
                  'gangpal','apetito','sed','defecac','miccion']

    def __init__(self, *args, **kwargs):
        super(EstadoMascotaForm, self).__init__(*args, **kwargs)
        self.fields['mascota'].widget.attrs.update({'class' : 'chosen'})
        self.fields['motivo'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fr'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fc'].widget.attrs.update({'class' : 'form-control'})
        self.fields['fp'].widget.attrs.update({'class' : 'form-control'})
        self.fields['t'].widget.attrs.update({'class' : 'form-control'})
        self.fields['exampiel'].widget.attrs.update({'class' : 'form-control'})
        self.fields['examucvis'].widget.attrs.update({'class' : 'form-control'})
        self.fields['gangpal'].widget.attrs.update({'class' : 'form-control'})
        self.fields['apetito'].widget.attrs.update({'class' : 'form-control'})
        self.fields['sed'].widget.attrs.update({'class' : 'form-control'})
        self.fields['defecac'].widget.attrs.update({'class' : 'form-control'})
        self.fields['miccion'].widget.attrs.update({'class' : 'form-control'})

class RequiredBaseInlineFormSet(BaseInlineFormSet):
    def clean(self):
        self.validate_unique()
        if any(self.errors):
            return
        if not self.forms[0].has_changed():
            raise forms.ValidationError("At least one %s is required" % self.model._meta.verbose_name)

VacunaFormSet = inlineformset_factory(Mascota, Vacuna, form=VacunaForm,formset=RequiredBaseInlineFormSet,extra=1,max_num=10)
DesparacitanteFormSet = inlineformset_factory(Mascota, Desparacitante, form=DesparacitanteForm,formset=RequiredBaseInlineFormSet,extra=1,max_num=10)
