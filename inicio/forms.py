from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Contacto, Cliente, Factura, Tarifas

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
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
        fields = '__all__'
        widgets = {
            'fecha_emision': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'fecha_vencimiento': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'fecha_actual': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
            'fecha_anterior': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Necesario para que Django use el formato correcto al mostrar fechas existentes
        for field in ['fecha_emision', 'fecha_vencimiento', 'fecha_actual', 'fecha_anterior']:
            self.fields[field].input_formats = ['%Y-%m-%d']

class TarifasForm(forms.ModelForm):

    class Meta:
        model=Tarifas
        fields='__all__'
