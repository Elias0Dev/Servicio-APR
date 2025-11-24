from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Contacto, Cliente, Factura, Tarifa, Cargo,Subsidio

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        exclude = ['id_contacto']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 5}),
        }

class ClienteForm(forms.ModelForm):

    class Meta:
        model=Cliente
        fields='__all__'

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['id_cliente', 'lectura_actual']  



class TarifaForm(forms.ModelForm):

    class Meta:
        model=Tarifa
        fields='__all__'
        widgets = {
            'fecha_inicio': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'fecha_fin': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
        }


class CargoForm(forms.ModelForm):

    class Meta:
        model=Cargo
        fields='__all__'

class SubsidioForm(forms.ModelForm):

    class Meta:
        model=Subsidio
        fields='__all__'
