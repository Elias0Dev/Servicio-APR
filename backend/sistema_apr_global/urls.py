"""
URL configuration for sistema_apr_global project.
"""
from django.contrib import admin
from django.urls import path, include
#api rest:
from rest_framework import routers
from inicio.api_views import ClienteViewSet, FacturaViewSet, TarifaViewSet, CargoViewSet,SubsidioViewSet,ContactoViewSet
# 👇 Única importación necesaria desde inicio, además de las de Django
from inicio import views as inicio_views

handler404 = 'inicio.views.page_404' 
router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'facturas', FacturaViewSet, basename='factura')
router.register(r'tarifas', TarifaViewSet, basename='tarifa')
router.register(r'cargos', CargoViewSet, basename='cargo')
router.register(r'subsidios', SubsidioViewSet, basename='subsidio')
router.register(r'contactos', ContactoViewSet, basename='contacto')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('inicio.urls')), 
    path('',include('pwa.urls')),

    path('api/', include(router.urls)),
]