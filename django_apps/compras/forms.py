from django import forms
from .models import CompraEmpresa

class CompraEmpresaForm(forms.ModelForm):
    class Meta:
        model = CompraEmpresa
        fields = ['proveedor','categoria','producto','cantidad','afecto','descuento']

    def __init__(self, *args, **kwargs):
        super(CompraEmpresaForm, self).__init__(*args, **kwargs)
        self.fields['proveedor'].widget.attrs.update({'class' : 'chosen'})
        self.fields['categoria'].widget.attrs.update({'class' : 'chosen'})
        self.fields['producto'].widget.attrs.update({'class' : 'chosen'})
        self.fields['cantidad'].widget.attrs.update({'class' : 'form-control input-mask','placeholder':'eg: 000.000.000.000.000,00'})
        self.fields['descuento'].widget.attrs.update({'class' : 'form-control input-mask','placeholder':'eg: 00000,00%','autocomplete':'off'})
