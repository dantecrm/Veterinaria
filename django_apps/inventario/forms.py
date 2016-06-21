from django import forms

from .models import Articulo, Categoria

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['nombre','marca','p_compra','p_venta','avatar']

    def __init__(self, *args, **kwargs):
        super(ArticuloForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
        self.fields['marca'].widget.attrs.update({'class' : 'form-control'})
        self.fields['p_compra'].widget.attrs.update({'class' : 'form-control input-mask','placeholder':'eg: 000.000.000.000.000,00'})
        self.fields['p_venta'].widget.attrs.update({'class' : 'form-control input-mask','placeholder':'eg: 000.000.000.000.000,00'})

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']
    def __init__(self, *args, **kwargs):
        super(CategoriaForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class' : 'form-control'})
