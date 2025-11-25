from rest_framework import serializers
from .models import Contacto, Cliente, Factura, Tarifa, Cargo,Subsidio

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'




class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'



class TarifaSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tarifa
        fields='__all__'



class CargoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Cargo
        fields='__all__'

class SubsidioSerializer(serializers.ModelSerializer):

    class Meta:
        model=Subsidio
        fields='__all__'
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'