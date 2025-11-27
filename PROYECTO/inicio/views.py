import pdfkit
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from datetime import date, timedelta
from .models import Factura, Cliente, Tarifa, Cargo, Subsidio
from .forms import ContactForm, ClienteForm, FacturaForm, TarifaForm, CargoForm, SubsidioForm

# --- Nuevas importaciones para gráficos ---
import matplotlib
matplotlib.use ('Agg')  # Usa un backend sin interfaz gráfica
import matplotlib.pyplot as plt
import base64
from io import BytesIO 

# 🔑 IMPORTACIONES NECESARIAS PARA AUTENTICACIÓN
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required 

from .perplexity import get_contextual_perplexity_response



#renderizado de vistas publicas


def page_404(request, exception=None):
    # exception=None para poder usarlo con DEBUG=True
    return render(request, '404.html', status=404)

def page_index(request):
    context = {}
    return render(request, 'inicio/index.html', context)

def page_consultaBoletas(request):
    context = {}
    return render(request, 'inicio/consulta_boletas.html', context)

def page_pago_en_linea(request):
    context = {}
    
    boleta_id = request.GET.get('boleta_id')
    if boleta_id:
        messages.info(request, f'Preparando pago para la boleta N° {boleta_id}.')
        
    return render(request, 'inicio/pago.html', context)

def page_contact(request):
    data = {
            'form': ContactForm()
        }
    if request.method == 'POST':
        formulario = ContactForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado correctamente"
        else:
            data["form"] = formulario
    return render(request, 'inicio/contacto.html', data)

#renderizado por modulos
#cliente
def agregar_cliente(request):

    data = {
        'form': ClienteForm()
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente agregado correctamente")
            return redirect(to="listar_cli")   
            
        else:
            data["form"] = formulario

    return render(request, 'cliente/agregar.html', data)

def listar_cliente(request):
    clientes= Cliente.objects.all()
    data = {
        'clientes':clientes
    }
    return render(request, 'cliente/listar.html', data)

def modificar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id_cliente=id)
    data = {
        'form': ClienteForm(instance=cliente)
    }
    #Deshabilitar el campo id_cliente
    data['form'].fields['id_cliente'].disabled = True
    
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST, instance=cliente)
        # Deshabilitar otra vez en el POST
        formulario.fields['id_cliente'].disabled = True
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Cliente modificado correctamente")
            return redirect(to="listar_cli")   
        data["form"] = formulario

    


    return render(request, 'cliente/modificar.html',data)

def eliminar_cliente(request, id):

    cliente = get_object_or_404(Cliente, id_cliente=id)
    cliente.delete()
    messages.success(request, "Cliente eliminado correctamente")
    return redirect(to="listar_cli")
   

#factura

def agregar_factura(request):
    data = {
        'form': FacturaForm()
    }

    if request.method == 'POST':
        formulario = FacturaForm(request.POST)


        if formulario.is_valid():
            factura = formulario.save(commit=False)

            hoy = date.today()

            # --- Buscar última factura del cliente ---
            ultima_factura = Factura.objects.filter(id_cliente=factura.id_cliente).order_by('-id_factura').first()
            # --- Rellenar factura anterior y fecha anterior ---
            if ultima_factura:
                factura.lectura_anterior = ultima_factura.lectura_actual
                factura.fecha_anterior = ultima_factura.fecha_actual
            else:
                factura.lectura_anterior = 0
                factura.fecha_anterior = hoy

            # --- Calcular consumo ---
            factura.consumo = factura.lectura_actual - factura.lectura_anterior

            # --- Fecha emisión / actual ---
            factura.fecha_emision = hoy
            factura.fecha_actual = hoy

            # --- Fecha de vencimiento ---
            factura.fecha_vencimiento = hoy + timedelta(days=21)

            # --- Calcular total a pagar ---
            cargo_fijo_ap = Cargo.objects.get(id_cargo=1).valor
            cargo_fijo_as = Cargo.objects.get(id_cargo=2).valor

            tarifa_ap = Tarifa.objects.filter(
                tipo='AP',
                rango_desde__lte=factura.consumo,
                rango_hasta__gte=factura.consumo
            ).first()
            valor_ap = tarifa_ap.cargo if tarifa_ap else 0
            tarifas_ap = factura.consumo * valor_ap

            tarifa_as = Tarifa.objects.filter(
                tipo='AS',
                rango_desde__lte=factura.consumo,
                rango_hasta__gte=factura.consumo
            ).first()
            valor_as = tarifa_as.cargo if tarifa_as else 0
            tarifas_as = factura.consumo * valor_as

            subsidio = Subsidio.objects.filter(cliente=factura.id_cliente).first()
            if subsidio:
                subsidio = subsidio.monto
                factura.subsidio=True
            else:
                subsidio = 0
                factura.subsidio=False

            pendiente = Factura.objects.filter(id_cliente=factura.id_cliente,estado_pago=False).count()
            
            if pendiente >= 2:
                factura.corte = True
                valor_corte= Cargo.objects.get(id_cargo=3).valor
            else:
                factura.corte = False
                valor_corte=0

            total=int(cargo_fijo_ap) + int(tarifas_ap) + int(cargo_fijo_as) +  int(tarifas_as) + int(valor_corte) - int(subsidio)



            factura.total_pagar = total

            

            # --- Estado inicial ---
            factura.estado_pago = False  # o False según tu lógica

            factura.save()

            data["mensaje"] = "Factura guardada correctamente"
            return redirect(to="listar_fact")   
        else:
            data["form"] = formulario

    return render(request, 'factura/agregar.html', data)


def listar_factura(request):
    factura= Factura.objects.all()
    data = {
        'factura': factura
    }
    return render(request, 'factura/listar.html', data)

def modificar_factura(request, id):

    factura = get_object_or_404(Factura, id_factura=id)
    data = {
        'form': FacturaForm(instance=factura)
    }
    #Deshabilitar el campo id_cliente
    data['form'].fields['id_cliente'].disabled = True
     
    if request.method == 'POST':
        formulario = FacturaForm(data=request.POST, instance=factura)
        # Deshabilitar otra vez en el POST
        formulario.fields['id_cliente'].disabled = True
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_fact")   
        data["form"] = formulario

    return render(request, 'factura/modificar.html',data)

def eliminar_factura(request, id):

    factura = get_object_or_404(Factura, id_factura=id)
    factura.delete()
    return redirect(to="listar_fact")
   
#tarifa
def agregar_tarifa(request):

    data = {
        'form': TarifaForm()
    }
    if request.method == 'POST':
        formulario = TarifaForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado correctamente"
            return redirect(to="listar_tari")   
        else:
            data["form"] = formulario

    return render(request, 'tarifa/agregar.html', data)

def listar_tarifa(request):
    tarifa= Tarifa.objects.all()
    data = {
        'tarifa': tarifa
    }
    return render(request, 'tarifa/listar.html', data)

def modificar_tarifa(request, id):

    tarifa = get_object_or_404(Tarifa, id_tarifa=id)
    data = {
        'form': TarifaForm(instance=tarifa)
    }
     
    if request.method == 'POST':
        formulario = TarifaForm(data=request.POST, instance=tarifa)
        
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_tari")   
        data["form"] = formulario

    return render(request, 'tarifa/modificar.html',data)

def eliminar_tarifa(request, id):

    tarifa = get_object_or_404(Tarifa, idtarifas=id)
    tarifa.delete()
    return redirect(to="listar_tari")

#cargo
def agregar_cargo(request):

    data = {
        'form': CargoForm()
    }
    if request.method == 'POST':
        formulario = CargoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado correctamente"
            return redirect(to="listar_cargo")   
        else:
            data["form"] = formulario

    return render(request, 'cargo/agregar.html', data)

def listar_cargo(request):
    cargo= Cargo.objects.all()
    data = {
        'cargo': cargo
    }
    return render(request, 'cargo/listar.html', data)

def modificar_cargo(request, id):

    cargo = get_object_or_404(Cargo, id_cargo=id)
    data = {
        'form': CargoForm(instance=cargo)
    }
     
    if request.method == 'POST':
        formulario = CargoForm(data=request.POST, instance=cargo)
        
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_cargo")   
        data["form"] = formulario

    return render(request, 'cargo/modificar.html',data)

def eliminar_cargo(request, id):

    cargo = get_object_or_404(cargo, id_cargo=id)
    cargo.delete()
    return redirect(to="listar_cargo")

#Subsidio:

def agregar_subsidio(request):

    data = {
        'form': SubsidioForm()
    }
    if request.method == 'POST':
        formulario = SubsidioForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data["mensaje"] = "Guardado correctamente"
            return redirect(to="listar_subsidio")   
        else:
            data["form"] = formulario

    return render(request, 'subsidio/agregar.html', data)

def listar_subsidio(request):
    subsidio= Subsidio.objects.all()
    data = {
        'subsidio': subsidio
    }
    return render(request, 'subsidio/listar.html', data)

def modificar_subsidio(request, id):

    subsidio = get_object_or_404(Subsidio, id_subsidio=id)
    data = {
        'form': SubsidioForm(instance=subsidio)
    }
     
    if request.method == 'POST':
        formulario = SubsidioForm(data=request.POST, instance=subsidio)
        
        if formulario.is_valid():
            formulario.save()
            return redirect(to="listar_subsidio")   
        data["form"] = formulario

    return render(request, 'subsidio/listar.html',data)

def eliminar_subsidio(request, id):

    subsidio = get_object_or_404(Subsidio, id_subsidio=id)
    subsidio.delete()
    return redirect(to="listar_subsidio")




def buscar_facturas_rut(request):
    rut = request.GET.get("rut", "").strip()
    context = {}

    if rut:
        try:
            cliente = Cliente.objects.get(rut=rut)

            facturas_pendientes = Factura.objects.filter(id_cliente=cliente, estado_pago=False)

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
    corte = factura.corte
    cargo_AP=Cargo.objects.get(id_cargo=1)
    cargo_AS=Cargo.objects.get(id_cargo=2)
    subsidio_habil=factura.subsidio
    subsidio = Subsidio.objects.filter(cliente=cliente).first()

    if subsidio_habil:
        subsidio = subsidio.monto

    else:
        subsidio = 0
        
        


    if corte:
        corte= Cargo.objects.get(id_cargo=3).valor
       
    else:
        corte=0
        


    tarifas_as = Tarifa.objects.filter(tipo='AS',rango_desde__lte=factura.consumo,rango_hasta__gte=factura.consumo).order_by('rango_desde')
    tarifas_ap = Tarifa.objects.filter(tipo='AP',rango_desde__lte=factura.consumo,rango_hasta__gte=factura.consumo).order_by('rango_desde')

    
    if tarifas_as.exists():  # Verifica que haya al menos un registro
        tarifa_as = tarifas_as.first()  # Toma el primer objeto
        
    if tarifas_ap.exists():  # Verifica que haya al menos un registro
        tarifa_ap = tarifas_ap.first()  # Toma el primer objeto


        

    valor_as= tarifa_as.cargo * factura.consumo      
    valor_ap= tarifa_ap.cargo * factura.consumo  
    
    
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
    tarifas_aplicadas = Tarifa.objects.filter(
        fecha_inicio__lte=factura.fecha_emision
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
        'chart_historico_b64': chart_historico_b64,
        'chart_desglose_b64': chart_desglose_b64,
        'mensaje_variacion': mensaje_variacion,
        'cargo_ap': cargo_AP,
        'cargo_as': cargo_AS,
        'corte': corte,
        'tarifa_as' : tarifa_as.cargo,
        'tarifa_ap' : tarifa_ap.cargo,
        'valor_ap' : valor_ap,
        'valor_as' : valor_as,
        'subsidio' : subsidio,
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

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=boleta_N°{factura.id_factura}.pdf'

    return response

#####CHATBOTT

from django.shortcuts import render
from django.http import JsonResponse
from .perplexity import get_contextual_perplexity_response

def mostrar_chatbot(request):
    return render(request, "inicio/perplexity.html")

import re

def extraer_numero_cliente(pregunta):
    # Buscar patrón que contenga alguna variante cercana a "mi número es" seguida de un número
    patron = r"mi\s*(n[uú]mero|num(?:ero)?)\s*es\s*(\d+)"
    match = re.search(patron, pregunta, re.IGNORECASE)
    if match:
        numero = match.group(2)
        return int(numero)
    return None

def api_chatbot(request):
    if request.method == "POST":
        pregunta = request.POST.get("message", "")
        numero_cliente = extraer_numero_cliente(pregunta.lower())

        pregunta_lower = pregunta.lower()
        descargar_boleta = (
            ('descargar' in pregunta_lower and 'boleta' in pregunta_lower) or
            'boleta pdf' in pregunta_lower or
            'descarga boleta' in pregunta_lower or
            'quiero boleta pdf' in pregunta_lower or
            ('descargar' in pregunta_lower and 'factura' in pregunta_lower) or
            'factura pdf' in pregunta_lower or
            'descarga factura' in pregunta_lower or
            'quiero factura pdf' in pregunta_lower
        )

        if numero_cliente:
            try:
                cliente = Cliente.objects.get(id_cliente=numero_cliente)
            except Cliente.DoesNotExist:
                return JsonResponse({"response": "No existe un cliente con ese número."})

            factura = Factura.objects.filter(id_cliente=cliente, estado=False).order_by('-fecha_emision').first()
            if not factura:
                return JsonResponse({"response": "No se encontraron facturas activas para tu cliente."})

            if descargar_boleta:
                # Aquí va toda la lógica para generar el PDF igual que antes
                cargo_AP = Cargo.objects.get(id_cargo=1)
                cargo_AS = Cargo.objects.get(id_cargo=2)
                subsidio = Subsidio.objects.filter(cliente=cliente).first()
                monto_subsidio = subsidio.monto if subsidio else 0
                estado_cliente = cliente.estado
                corte = Cargo.objects.get(id_cargo=3).valor if estado_cliente == "corte" else 0

                tarifas_as = Tarifa.objects.filter(tipo='AS', rango_desde__lte=factura.consumo, rango_hasta__gte=factura.consumo).order_by('rango_desde')
                tarifas_ap = Tarifa.objects.filter(tipo='AP', rango_desde__lte=factura.consumo, rango_hasta__gte=factura.consumo).order_by('rango_desde')

                tarifa_as = tarifas_as.first() if tarifas_as.exists() else None
                tarifa_ap = tarifas_ap.first() if tarifas_ap.exists() else None

                valor_as = tarifa_as.cargo * factura.consumo if tarifa_as else 0
                valor_ap = tarifa_ap.cargo * factura.consumo if tarifa_ap else 0

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

                contexto = {
                    'factura': factura,
                    'cliente': cliente,
                    'cargo_ap': cargo_AP,
                    'cargo_as': cargo_AS,
                    'subsidio': monto_subsidio,
                    'corte': corte,
                    'tarifa_as': tarifas_as,
                    'tarifa_ap': tarifas_ap,
                    'valor_ap': valor_ap,
                    'valor_as': valor_as,
                    'chart_historico_b64': chart_historico_b64,
                }

                html = render_to_string('inicio/boleta.html', contexto)
                path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
                config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                options = {
                    'page-size': 'A4',
                    'encoding': 'UTF-8',
                    'margin-top': '0.75in',
                    'margin-bottom': '0.75in',
                    'margin-left': '0.75in',
                    'margin-right': '0.75in',
                }
                pdf = pdfkit.from_string(html, False, options=options, configuration=config)

                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename=boleta_N°{factura.id_factura}.pdf'
                return response

            else:
                respuesta = (
                    f"Hola {cliente.nombre}, tu última factura fue emitida el "
                    f"{factura.fecha_emision.strftime('%d-%m-%Y')} con un total a pagar de ${factura.total_pagar}. "
                    f"Si deseas descargar la boleta en PDF, por favor indícalo."
                )
                return JsonResponse({"response": respuesta})

        else:
            respuesta = get_contextual_perplexity_response(pregunta)
            return JsonResponse({"response": respuesta})

    return JsonResponse({"error": "Método no permitido"}, status=405)
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


import joblib
from django.http import JsonResponse

# Cargar modelo ML al importar módulo (ajusta la ruta según tu proyecto)
modelo_ml = joblib.load('ml_model\modelo_clasificacion_consumo.pkl')

def prediccion_estado_pago(request, id):
    try:
        factura = Factura.objects.get(id_factura=id)
    except Factura.DoesNotExist:
        return JsonResponse({'error': 'Factura no encontrada'}, status=404)

    datos = [
        float(factura.total_pagar),
        factura.consumo,
        int(factura.subsidio),
        int(factura.corte),
        (factura.fecha_vencimiento - factura.fecha_emision).days
    ]

    probabilidad = modelo_ml.predict_proba([datos])[0][1]
    clase_predicha = modelo_ml.predict([datos])[0]

    resultado = {
        'factura_id': id,
        'probabilidad_pago': probabilidad,
        'prediccion': 'Paga' if clase_predicha == 1 else 'No paga'
    }
    return JsonResponse(resultado)
