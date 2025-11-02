from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("deatlle-boletas/", views.consultaBoletas, name="consultaBoletas"),
]