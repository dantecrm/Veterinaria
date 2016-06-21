from django import forms
from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory
from .models import OrdenVenta, CarritoVenta

class OrdenVentaForm(forms.ModelForm):
    class Meta:
        model = OrdenVenta
        fields = ['cliente']

    def __init__(self, *args, **kwargs):
        super(OrdenVentaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].widget.attrs.update({'class' : 'chosen'})
        # cliente = self.instance.cliente
        # self.fields['cliente'].queryset = Cliente.objects.get(slug = cliente.slug)

class CarritoVentaForm(forms.ModelForm):
    class Meta:
        model = CarritoVenta
        fields = ['producto','cantidad']

    def __init__(self, *args, **kwargs):
        super(CarritoVentaForm, self).__init__(*args, **kwargs)
        self.fields['producto'].widget.attrs.update({'class' : 'chosen'})
        self.fields['cantidad'].widget.attrs.update({'class' : 'form-control input-mask','placeholder':'eg: 000.000.000.000.000,00'})

CarritoVentaFormset = inlineformset_factory(OrdenVenta,CarritoVenta,
                                            form=CarritoVentaForm,extra=1, max_num=10)

