from django.urls import path

from . import views

urlpatterns = [
    path("", views.page_index, name="page_index"),
    path("detalle-boletas/", views.page_consultaBoletas, name="page_consultaBoletas"),
    path('api/facturas/', views.buscar_facturas, name='buscar_facturas'),
    path('pago/', views.page_pago_en_linea, name='page_pago_en_linea'),
    path('buscar_facturas_rut/', views.buscar_facturas_rut, name='buscar_facturas_rut'),
    path('generar_boleta/<int:id_factura>/pdf/', views.generar_boleta_pdf, name='generar_boleta_pdf'),
    path('contacto/', views.page_contact, name='page_contacto'),
    # 🔑 NUEVA URL DE REGISTRO
    path('registro/', views.registro_usuario, name='registro'),
]