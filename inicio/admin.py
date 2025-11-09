from django.contrib import admin

class ClienteAdmin(admin.ModelAdmin):
    list_display=['id_cliente', 'rut', 'dv', 'nombre', 'direccion', 'telefono', 'email', 'numero_medidor']
    list_editable = ['rut','nombre','dv','direccion', 'telefono', 'email', 'numero_medidor']
    search_fields = ['rut', 'nombre']
    list_per_page = 5


class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id_factura', 'id_cliente', 'consumo', 'estado']
    list_editable = ['consumo', 'estado']
    list_filter = ['estado']
    list_per_page = 5


# Register your models here.
from .models import Cliente, Factura, Tarifas, Contacto

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Tarifas)
admin.site.register(Contacto)