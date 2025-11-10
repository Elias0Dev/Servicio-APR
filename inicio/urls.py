from django.urls import path

from . import views

urlpatterns = [
    path("", views.page_index, name="page_index"),
    path("detalle_boletas/", views.page_consultaBoletas, name="page_consultaBoletas"),
    path('api/facturas/', views.buscar_facturas, name='buscar_facturas'),
    path('pago/', views.page_pago_en_linea, name='page_pago_en_linea'),
    path('buscar_facturas_rut/', views.buscar_facturas_rut, name='buscar_facturas_rut'),
    path('generar_boleta/<int:id_factura>/pdf/', views.generar_boleta_pdf, name='generar_boleta_pdf'),
    path('contacto/', views.page_contact, name='page_contacto'),
    path('buscar_facturas/', views.buscar_facturas, name='buscar_facturas_api'),

    path("cliente/agregar_cliente/", views.agregar_cliente, name="agregar_cli"),
    path("cliente/listar_cliente/", views.listar_cliente, name="listar_cli"),
    path("cliente/modificar_cliente/<id>/", views.modificar_cliente, name="modificar_cli"),
    path("cliente/eliminar_cliente/<id>/", views.eliminar_cliente, name="eliminar_cli"),

    path("factura/agregar_factura/", views.agregar_factura, name="agregar_fact"),
    path("factura/listar_factura/", views.listar_factura, name="listar_fact"),
    path("factura/modificar_factura/<id>/", views.modificar_factura, name="modificar_fact"),
    path("factura/eliminar_factura/<id>/", views.eliminar_factura, name="eliminar_fact"),

    path("tarifa/agregar_tarifa/", views.agregar_tarifa, name="agregar_tari"),
    path("tarifa/listar_tarifas/", views.listar_tarifa, name="listar_tari"),
    path("tarifa/modificar_tarifas/<id>/", views.modificar_tarifa, name="modificar_tari"),
    path("tarifa/eliminar_tarifas/<id>/", views.eliminar_tarifa, name="eliminar_tari"),

    path("fija/agregar_tarifa_fija/", views.agregar_tarifa_fija, name="agregar_fija"),
    path("fija/listar_tarifas_fija/", views.listar_tarifa_fija, name="listar_fija"),
    path("fija/modificar_tarifas_fija/<id>/", views.modificar_tarifa_fija, name="modificar_fija"),
    path("fija/eliminar_tarifas_fija/<id>/", views.eliminar_tarifa_fija, name="eliminar_fija"),


]