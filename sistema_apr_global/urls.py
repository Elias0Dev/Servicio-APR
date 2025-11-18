"""
URL configuration for sistema_apr_global project.
"""
from django.contrib import admin
from django.urls import path, include
# 👇 Única importación necesaria desde inicio, además de las de Django
from inicio import views as inicio_views 


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. AUTENTICACIÓN: Agrupamos Login/Logout y Registro bajo '/cuentas/'
    path('cuentas/', include([
        
        # a) Login, Logout, Cambio de Contraseña de Django
        path('login/', include('django.contrib.auth.urls')), 
        
        # b) Registro (Llamamos a tu vista personalizada)
        path('registro/', inicio_views.registro_usuario, name='registro'),
    ])),
    
    # 3. Tus demás rutas
    path('', include('inicio.urls')), 
    path('',include('pwa.urls')),
]