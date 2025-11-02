from django.shortcuts import render
from django.http import JsonResponse
from .models import Factura

def index(request):
    context={}
    return render(request, 'inicio/index.html',context)

def consultaBoletas(request):
    context={}
    return render(request, 'inicio/consulta-boletas.html',context)




def buscar_facturas(request):
    numero_cliente = request.GET.get('numero_cliente')

    if not numero_cliente:
        return JsonResponse({'error': 'No se proporcionó número de cliente'}, status=400)

    # Filtrar facturas por cliente
    facturas = Factura.objects.filter(id_cliente=numero_cliente).order_by('-fecha_emision')
    
    # Convertir a lista de diccionarios
    data = []
    for f in facturas:
        data.append({
            'consumido': f'Consumo: {f.consumo}',  # puedes personalizar
            'fecha': f.fecha_emision.strftime('%Y-%m-%d'),
            'valor': f"${f.total_pagar:.2f}"
        })
    
    return JsonResponse({'facturas': data})
