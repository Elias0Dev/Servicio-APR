from django.contrib import admin

# Register your models here.
from .models import Cliente, Factura, Tarifas, Contacto

admin.site.register(Cliente)
admin.site.register(Factura)
admin.site.register(Tarifas)
admin.site.register(Contacto)