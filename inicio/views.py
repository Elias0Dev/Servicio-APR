from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
from transbank.common.options import WebpayOptions
from transbank.error.transaction_create_error import TransactionCreateError

from .models import Factura, Cliente
from decimal import Decimal


def page_index(request):
    context = {}
    return render(request, 'inicio/index.html', context)


def page_consultaBoletas(request):
    context = {}
    return render(request, 'inicio/consulta-boletas.html', context)


def page_pago_en_linea(request):
    context = {}
    return render(request, 'inicio/pago.html', context)


def buscar_facturas(request):
    numero_cliente = request.GET.get('numero_cliente')

    if not numero_cliente:
        return JsonResponse({'error': 'No se proporcionó número de cliente'}, status=400)

    facturas = Factura.objects.filter(id_cliente=numero_cliente).order_by('-fecha_emision')

    data = []
    for f in facturas:
        data.append({
            'consumido': f.consumo,
            'fecha': f.fecha_emision.strftime('%Y-%m-%d'),
            'valor': f"${format(int(f.total_pagar), ',d').replace(',', '.')}"
        })

    return JsonResponse({'facturas': data})


def buscar_facturas_rut(request):
    rut = request.GET.get("rut", "").strip()
    context = {}

    if rut:
        try:
            # Buscamos el cliente por RUT (sin DV)
            cliente = Cliente.objects.get(rut=rut)

            # Facturas con estado=False → pendientes
            facturas_pendientes = Factura.objects.filter(id_cliente=cliente, estado=False)

            context["cliente"] = cliente
            context["facturas"] = facturas_pendientes

            if not facturas_pendientes.exists():
                context["mensaje"] = "No se encontraron facturas pendientes para este cliente."
        except Cliente.DoesNotExist:
            context["error"] = "No existe un cliente registrado con ese RUT."
    else:
        context["error"] = "Debe ingresar un RUT para realizar la búsqueda."

    # Renderizamos en pago.html
    return render(request, "inicio/pago.html", context)

