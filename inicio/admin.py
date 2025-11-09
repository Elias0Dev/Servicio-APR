from django.contrib import admin
# Asegúrate de que todos los modelos que registras están importados
from .models import Cliente, Factura, Contacto, Tarifas

# 1. Administración para el modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # CORREGIDO: 'id_medidor' -> 'numero_medidor', 'es_vigente' -> 'vigente'
    list_display = (
        'id_cliente', 
        'rut', 
        'nombre', 
        'apellido', 
        'direccion', 
        'numero_medidor', # Nombre correcto del campo en models.py
        'vigente' # Nombre correcto del campo en models.py
    )
    # Campos por los que se puede buscar (CORREGIDO: usando 'numero_medidor')
    search_fields = ('rut', 'nombre', 'apellido', 'numero_medidor')
    # Filtros laterales (CORREGIDO: usando 'vigente')
    list_filter = ('vigente',)
    # Hacer el campo 'rut' clickeable para entrar al detalle
    list_display_links = ('rut',)
    # Permite editar el campo directamente en la lista (CORREGIDO: usando 'vigente')
    list_editable = ('vigente',)


# 2. Administración para el modelo Factura
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de Facturas.
    list_display = (
        'id_factura', 
        'id_cliente', 
        'fecha_emision', 
        'fecha_vencimiento', 
        'consumo', 
        'total_pagar', 
        'estado',
        'tarifa_aplicada' # Asumiendo este campo en models.py
    )
    # Filtros laterales
    list_filter = ('estado', 'fecha_emision', 'fecha_vencimiento')
    # Campos por los que se puede buscar
    search_fields = (
        'id_factura', 
        'id_cliente__rut', 
        'id_cliente__nombre', 
        'id_cliente__apellido' 
    )
    # Campos para la edición de detalles
    fieldsets = (
        ('Información de la Factura', {
            'fields': (
                'id_cliente', 
                'fecha_emision', 
                'fecha_vencimiento', 
                'consumo', 
                'estado',
                'lectura_anterior', 
                'lectura_actual',   
                'fecha_anterior',   
                'fecha_actual',     
            )
        }),
        ('Cálculos', {
            'fields': ('total_pagar', 'tarifa_aplicada') 
        }),
    )
    # Ordenar por defecto por fecha de emisión descendente
    ordering = ('-fecha_emision',)


# 3. Administración para el modelo Contacto
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    # CORREGIDO: 'id_contacto' -> 'id', 'correo' -> 'email', 'fecha_envio' -> 'creado_el'
    list_display = (
        'id', # Usando el PK por defecto
        'nombre', 
        'email', # Nombre correcto del campo en models.py
        'creado_el', # Nombre correcto del campo en models.py
        'revisado'
    )
    # Filtros laterales (CORREGIDO: usando 'creado_el')
    list_filter = ('revisado', 'creado_el')
    # Campos por los que se puede buscar (CORREGIDO: usando 'email')
    search_fields = ('nombre', 'email', 'asunto')
    # Permite editar el estado de revisión directamente en la lista
    list_editable = ('revisado',)
    # Solo lectura en el detalle (CORREGIDO: usando 'email' y 'creado_el')
    readonly_fields = ('nombre', 'email', 'asunto', 'mensaje', 'creado_el')

# 4. Administración para el modelo Tarifas
@admin.register(Tarifas)
class TarifasAdmin(admin.ModelAdmin):
    # CORREGIDO: 'id_tarifa' -> 'idtarifas', 'valor_m3' -> 'cargo'
    list_display = (
        'idtarifas', # Nombre correcto del campo en models.py
        'rango_desde', 
        'rango_hasta', 
        'cargo', # Nombre correcto del campo en models.py
        'fecha_inicio', 
        'fecha_fin'
    )
    # Campos por los que se puede buscar (CORREGIDO: usando 'cargo')
    search_fields = ('cargo',)
    # Filtros laterales
    list_filter = ('tipo', 'fecha_inicio', 'fecha_fin') # Asumo que 'tipo' se puede filtrar
