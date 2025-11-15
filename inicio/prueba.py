import pdfkit
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse,  HttpResponse
from django.template.loader import render_to_string
from datetime import date, timedelta
from .models import Factura, Cliente, Tarifa, Cargo, Subsidio
from .forms import ContactForm, ClienteForm, FacturaForm, TarifaForm, CargoForm, SubsidioForm
# --- Nuevas importaciones para gráficos ---
import matplotlib
matplotlib.use('Agg')  # Usa un backend sin interfaz gráfica
import matplotlib.pyplot as plt
import base64
from io import BytesIO 
