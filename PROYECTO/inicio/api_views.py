from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contacto, Cliente, Factura, Tarifa, Cargo,Subsidio
from .serializers import ClienteSerializer, FacturaSerializer, TarifaSerializer,CargoSerializer, SubsidioSerializer, ContactSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    lookup_field = 'id_cliente'   # IMPORTANTE


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    lookup_field = 'id_factura'   # IMPORTANTE
    filterset_fields = ['id_cliente', 'fecha_emision', 'estado_pago']

class TarifaViewSet(viewsets.ModelViewSet):
    queryset = Tarifa.objects.all()
    serializer_class = TarifaSerializer
    lookup_field = 'id_tarifa'   # IMPORTANTE

class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    lookup_field = 'id_cargo'   # IMPORTANTE

class SubsidioViewSet(viewsets.ModelViewSet):
    queryset = Subsidio.objects.all()
    serializer_class = SubsidioSerializer
    lookup_field = 'id_subsidio'   # IMPORTANTE

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ContactSerializer
    lookup_field = 'id_contacto'   # IMPORTANTE