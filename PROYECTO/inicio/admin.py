from django.contrib import admin
# Asegúrate de que todos los modelos que registras están importados
from .models import Cliente, Factura, Contacto, Tarifa

class ClienteAdmin(admin.ModelAdmin):
    list_display=['id_cliente', 'rut', 'dv', 'nombre', 'direccion', 'telefono', 'email', 'numero_medidor']
    list_editable = ['rut','nombre','dv','direccion', 'telefono', 'email', 'numero_medidor']
    search_fields = ['rut', 'nombre']
    list_per_page = 5


class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id_factura', 'id_cliente', 'consumo', 'estado_pago', 'subsidio']
    list_editable = ['consumo', 'estado_pago', 'subsidio']
    list_filter = ['subsidio']
    search_fields = ['id_factura']
    list_per_page = 5




# Register your models here.
from .models import Cliente, Factura, Tarifa, Contacto,Cargo,Subsidio

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Tarifa)
admin.site.register(Cargo)
admin.site.register(Subsidio)
admin.site.register(Contacto)
