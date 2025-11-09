import pdfkit
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse,  HttpResponse
from django.template.loader import render_to_string
from .models import Factura, Cliente, Tarifas
from .forms import ContactForm
# --- Nuevas importaciones para gráficos ---
import matplotlib
matplotlib.use('Agg')  # Usa un backend sin interfaz gráfica
import matplotlib.pyplot as plt
import base64
from io import BytesIO

def page_index(request):
    context = {}
    return render(request, 'inicio/index.html', context)

def page_consultaBoletas(request):
    context = {}
    return render(request, 'inicio/consulta_boletas.html', context)

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
    try:
        cliente = Cliente.objects.get(id_cliente=numero_cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Número de cliente no encontrado'}, status=404)

    facturas = Factura.objects.filter(id_cliente=numero_cliente).order_by('-fecha_emision')

    data = []
    for f in facturas:
        data.append({
            'consumido': f.consumo,
            'fecha': f.fecha_emision.strftime('%Y-%m-%d'),
            'valor': f"${format(int(f.total_pagar), ',d').replace(',', '.')}",
            'id': f.id_factura
        })
    # --- NUEVO: Preparar datos para el gráfico de progreso ---
    consumo_reciente_data = None
    factura_reciente = facturas.first() # Obtiene la factura más reciente

    if factura_reciente:
        # Límite de referencia. Puedes hacerlo dinámico (ej. un campo en el modelo Cliente)
        LIMITE_MENSUAL = 35  
        consumo_actual = factura_reciente.consumo
        
        porcentaje = 0
        if LIMITE_MENSUAL > 0:
            # Se calcula el porcentaje y se redondea
            porcentaje = round((consumo_actual / LIMITE_MENSUAL) * 100)

        consumo_reciente_data = {
            'consumo': consumo_actual,
            'limite': LIMITE_MENSUAL,
            'porcentaje': porcentaje,
            # Se usa el formato de fecha que prefieras
            'periodo': factura_reciente.fecha_emision.strftime('%B %Y').capitalize()
        }
    return JsonResponse({
        'nombre_cliente': cliente.nombre,
        'facturas': data,
        'consumo_reciente': consumo_reciente_data  # Se añaden los datos del gráfico
    })

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
    # --- GRÁFICO 1: HISTORIAL DE CONSUMO (ÚLTIMOS 6 MESES) ---
    facturas_historial = Factura.objects.filter(id_cliente=cliente).order_by('-fecha_emision')[:6]
    meses = [f.fecha_emision.strftime('%b %Y') for f in reversed(facturas_historial)]
    consumos = [f.consumo for f in reversed(facturas_historial)]

    fig, ax = plt.subplots(figsize=(8, 3))
    ax.bar(meses, consumos, color='#007bff')
    ax.set_ylabel('Consumo (m³)')
    ax.set_title('Historial de Consumo', fontsize=10)
    plt.xticks(rotation=45, ha="right", fontsize=8)
    plt.yticks(fontsize=8)
    plt.tight_layout()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    chart_historico_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close(fig)
    # -----------------------------------------------------------

    fig, ax = plt.subplots(figsize=(8, 3))
    plt.close(fig)

    # --- INICIO: CÁLCULO DE VARIACIÓN DE CONSUMO ---
    mensaje_variacion = ""
    # Se necesitan al menos 2 meses de historial para comparar
    if len(consumos) > 1:
        consumo_actual = consumos[-1]
        consumo_anterior = consumos[-2]
        
        if consumo_anterior > 0:
            variacion_pct = ((consumo_actual - consumo_anterior) / consumo_anterior) * 100
            # Se genera un mensaje distinto si el consumo sube, baja o se mantiene
            if variacion_pct > 1: # Un aumento significativo
                mensaje_variacion = f"Este mes tu consumo fue un <strong class='aumento'>{variacion_pct:.0f}% mayor</strong> al del mes anterior."
            elif variacion_pct < -1: # Una disminución significativa
                mensaje_variacion = f"Este mes tu consumo fue un <strong class='disminucion'>{abs(variacion_pct):.0f}% menor</strong> al del mes anterior."
            else:
                mensaje_variacion = "Tu consumo se mantuvo <strong>estable</strong> respecto al mes anterior."
        elif consumo_actual > 0:
            mensaje_variacion = "El mes pasado no registraste consumo."

    # --- GRÁFICO 2: DESGLOSE DE CONSUMO POR TRAMO NO TOMAR EN CUENTA NO SUPE SACARLO SIN CAGAR EL CODIGO XD ---
    tarifas_aplicadas = Tarifas.objects.filter(
        fecha_inicio__lte=factura.fecha_emision,
        fecha_fin__gte=factura.fecha_emision
    ).order_by('rango_desde')
    
    consumo_total = int(factura.consumo)
    labels_tramos = []
    consumo_por_tramo = []
    restante = consumo_total
    
    for t in tarifas_aplicadas:
        desde, hasta = int(t.rango_desde), int(t.rango_hasta)
        capacidad_tramo = max(0, hasta - desde) # Ajustado para rangos
        usado = min(restante, capacidad_tramo) if restante > 0 else 0
        
        if usado > 0:
            labels_tramos.append(f"Tramo {desde}-{hasta} m³")
            consumo_por_tramo.append(usado)
        
        restante -= usado
    
    if restante > 0: # Si queda consumo fuera de los tramos definidos
        labels_tramos.append("Otros Tramos")
        consumo_por_tramo.append(restante)
    
    chart_desglose_b64 = None
    if consumo_por_tramo and sum(consumo_por_tramo) > 0:
        fig2, ax2 = plt.subplots(figsize=(8, 3.5))
        wedges, texts, autotexts = ax2.pie(consumo_por_tramo, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
        ax2.axis('equal')
        ax2.set_title('Desglose de Consumo del Mes', fontsize=10)
        ax2.legend(wedges, labels_tramos, title="Tramos", loc="center left", bbox_to_anchor=(0.9, 0, 0.5, 1), fontsize=8)
        plt.setp(autotexts, size=8, weight="bold")
        
        buffer2 = BytesIO()
        plt.savefig(buffer2, format='png', bbox_inches='tight')
        buffer2.seek(0)
        chart_desglose_b64 = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        plt.close(fig2)
    # --------------------------------------------------------------

    contexto = {
        'factura': factura,
        'cliente': cliente,
        'tarifas_aplicadas': tarifas_aplicadas,
        'chart_historico_b64': chart_historico_b64,
        'chart_desglose_b64': chart_desglose_b64,
        'mensaje_variacion': mensaje_variacion,
    }
    # Renderizar el HTML como string
    html = render_to_string('inicio/boleta.html', contexto)
    # Opciones de PDF
    options = {
        'page-size': 'A4', 'encoding': 'UTF-8',
        'margin-top': '0.75in', 'margin-bottom': '0.75in',
        'margin-left': '0.75in', 'margin-right': '0.75in',
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




