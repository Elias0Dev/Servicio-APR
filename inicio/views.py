import pdfkit
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
# 🔑 IMPORTACIONES NECESARIAS PARA AUTENTICACIÓN
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required 

# Asegúrate de que estas importaciones son correctas para tu proyecto
from .models import Factura, Cliente, Tarifas
from .forms import ContactForm

def page_index(request):
    context = {}
    return render(request, 'inicio/index.html', context)


def page_consultaBoletas(request):
    """
    Maneja la visualización del formulario de consulta de boletas (GET) 
    y el procesamiento de la búsqueda por número de cliente (POST).
    """
    context = {
        'boletas': [],
        'cliente_encontrado': False,
        'form_submitted': False,
        'numero_cliente': '',
        'nombre_cliente': None,
    }

    if request.method == 'POST':
        numero_cliente = request.POST.get('numero_cliente', '').strip()
        context['numero_cliente'] = numero_cliente
        context['form_submitted'] = True

        if numero_cliente:
            try:
                # 1. Buscar el cliente por el NUC (Número de Cliente)
                cliente = Cliente.objects.get(id=numero_cliente) 
                
                # Cliente encontrado
                context['cliente_encontrado'] = True
                context['nombre_cliente'] = f"{cliente.nombre} {cliente.apellido}" if hasattr(cliente, 'apellido') else cliente.nombre

                # 2. Buscar facturas asociadas a ese cliente (Pendientes y Pagadas)
                facturas_db = Factura.objects.filter(id_cliente=cliente).order_by('-fecha_emision')

                # 3. Formatear los datos para la plantilla
                boletas_data = []
                for factura in facturas_db:
                    estado_pago = 'Pagada' if factura.estado else 'Pendiente'
                    
                    boletas_data.append({
                        'id': factura.id_factura, 
                        'numero': factura.id_factura, 
                        'periodo': factura.fecha_emision.strftime('%Y-%m'), 
                        'monto': factura.total_pagar, 
                        'estado': estado_pago,
                        'consumo': factura.consumo,
                        'fecha_vencimiento': factura.fecha_vencimiento.strftime('%d/%m/%Y') if hasattr(factura, 'fecha_vencimiento') and factura.fecha_vencimiento else 'N/A',
                        'fecha_pago': factura.fecha_pago.strftime('%d/%m/%Y') if factura.estado and factura.fecha_pago else None,
                    })

                context['boletas'] = boletas_data

                if not boletas_data:
                    messages.success(request, f'Cliente {numero_cliente} encontrado, pero no se registraron boletas históricas.')

            except Cliente.DoesNotExist:
                context['cliente_encontrado'] = False
                messages.error(request, f'No se encontró un cliente con el NUC: {numero_cliente}. Verifique el número e intente de nuevo.')
            
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar la búsqueda: {e}')
        else:
            messages.warning(request, 'Debe ingresar un Número de Cliente (NUC).')


    return render(request, 'inicio/consulta-boletas.html', context)


def page_pago_en_linea(request):
    context = {}
    
    boleta_id = request.GET.get('boleta_id')
    if boleta_id:
        messages.info(request, f'Preparando pago para la boleta N° {boleta_id}.')
        
    return render(request, 'inicio/pago.html', context)

def page_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje enviado exitosamente.')
            return redirect('page_contacto')
    else:
        form = ContactForm()
    return render(request, 'inicio/contacto.html', {'form': form})


def buscar_facturas(request):
    numero_cliente = request.GET.get('numero_cliente')

    if not numero_cliente:
        return JsonResponse({'error': 'No se proporcionó número de cliente'}, status=400)

    try:
        cliente_obj = Cliente.objects.get(id=numero_cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({'error': 'Cliente no encontrado'}, status=404)

    facturas = Factura.objects.filter(id_cliente=cliente_obj).order_by('-fecha_emision')

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
            cliente = Cliente.objects.get(rut=rut)

            facturas_pendientes = Factura.objects.filter(id_cliente=cliente, estado=False)

            context["cliente"] = cliente
            context["facturas"] = facturas_pendientes

            if not facturas_pendientes.exists():
                context["mensaje"] = "No se encontraron facturas pendientes para este cliente."
        except Cliente.DoesNotExist:
            context["error"] = "No existe un cliente registrado con ese RUT."
    else:
        context["error"] = "Debe ingresar un RUT para realizar la búsqueda."

    return render(request, "inicio/pago.html", context)

def generar_boleta_pdf(request, id_factura):
    factura = Factura.objects.get(id_factura=id_factura)
    cliente = factura.id_cliente
    tarifas_aplicadas = Tarifas.objects.filter(
        fecha_inicio__lte=factura.fecha_emision,
        fecha_fin__gte=factura.fecha_emision
    ).order_by('rango_desde')

    html = render_to_string('inicio/boleta.html', {
        'factura': factura,
        'cliente': cliente,
        'tarifas_aplicadas': tarifas_aplicadas
    })

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

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=boleta_N°{factura.id_factura}.pdf'

    return response

# ----------------------------------------------------------------------
# VISTAS DE AUTENTICACIÓN Y PERFIL
# ----------------------------------------------------------------------

# 🔑 VISTA DE PERFIL (Protegida)
@login_required(login_url='/cuentas/login/')
def perfil(request):
    """
    Renderiza la página de perfil del usuario, accesible después del login.
    """
    
    nombre_usuario = request.user.username 

    context = {
        'nombre_usuario': nombre_usuario,
    }
    
    # Renderiza la plantilla: inicio/templates/inicio/perfil.html
    return render(request, 'inicio/perfil.html', context)


# 🔑 VISTA DE REGISTRO
def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            # Redirige a /accounts/profile/ (o lo que LOGIN_REDIRECT_URL defina)
            return redirect(settings.LOGIN_REDIRECT_URL) 
    else:
        form = UserCreationForm()
        
    return render(request, 'registration/registro.html', {'form': form})