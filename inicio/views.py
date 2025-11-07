import pdfkit
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse,  HttpResponse
from django.template.loader import render_to_string
from .models import Factura, Cliente, Tarifas
from .forms import ContactForm

def page_index(request):
    context = {}
    return render(request, 'inicio/index.html', context)


def page_consultaBoletas(request):
    context = {}
    return render(request, 'inicio/consulta-boletas.html', context)


def page_pago_en_linea(request):
    context = {}
    return render(request, 'inicio/pago.html', context)

def page_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda en la base de datos
            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('page_contacto')  # Redirige a la misma página
    else:
        form = ContactForm()
    return render(request, 'inicio/contacto.html', {'form': form})



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
            'valor': f"${format(int(f.total_pagar), ',d').replace(',', '.')}",
            'id': f.id_factura
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

def generar_boleta_pdf(request, id_factura):
    # Obtener factura y datos relacionados
    factura = Factura.objects.get(id_factura=id_factura)
    cliente = factura.id_cliente
    tarifas_aplicadas = Tarifas.objects.filter(
        fecha_inicio__lte=factura.fecha_emision,
        fecha_fin__gte=factura.fecha_emision
    ).order_by('rango_desde')

    # Renderizar el HTML como string
    html = render_to_string('inicio/boleta.html', {
        'factura': factura,
        'cliente': cliente,
        'tarifas_aplicadas': tarifas_aplicadas
    })

    # Opciones de PDF
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'margin-right': '0.75in',
    }

    # Configuración de pdfkit para Windows
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Generar PDF en memoria
    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    # Devolver PDF como respuesta
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=boleta_N°{factura.id_factura}.pdf'

    return response




