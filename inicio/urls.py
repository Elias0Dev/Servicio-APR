from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.page_index, name="page_index"),
    path("detalle_boletas/", views.page_consultaBoletas, name="page_consultaBoletas"),
    path('detalle_boletas/facturas/', views.buscar_facturas, name='buscar_facturas'),
    path('pago/', views.page_pago_en_linea, name='page_pago_en_linea'),
    path('buscar_facturas_rut/', views.buscar_facturas_rut, name='buscar_facturas_rut'),
    path('generar_boleta/<int:id_factura>/pdf/', views.generar_boleta_pdf, name='generar_boleta_pdf'),
    path('contacto/', views.page_contact, name='page_contacto'),
    path('buscar_facturas/', views.buscar_facturas, name='buscar_facturas_api'),
    #CRUD
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

    path("cargo/agregar_cargo/", views.agregar_cargo, name="agregar_cargo"),
    path("cargo/listar_cargo/", views.listar_cargo, name="listar_cargo"),
    path("cargo/modificar_cargo/<id>/", views.modificar_cargo, name="modificar_cargo"),
    path("cargo/eliminar_cargo/<id>/", views.eliminar_cargo, name="eliminar_cargo"),

    path("subsidio/agregar_subsidio/", views.agregar_subsidio, name="agregar_subsidio"),
    path("subsidio/listar_subsidio/", views.listar_subsidio, name="listar_subsidio"),
    path("subsidio/modificar_subsidio/<id>/", views.modificar_subsidio, name="modificar_subsidio"),
    path("subsidio/eliminar_subsidio/<id>/", views.eliminar_subsidio, name="eliminar_subsidio"),

    path('perplexity/', views.mostrar_chatbot, name='mostrar_chatbot'),
    path('perplexity/api/', views.api_chatbot, name='api_chatbot'),
    
    # Usuario
    path('accounts/profile/', views.perfil, name='perfil'),
]