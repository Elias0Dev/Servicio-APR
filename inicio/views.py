from django.shortcuts import render

def index(request):
    context={}
    return render(request, 'inicio/inicio_sesion.html',context)
# Create your views here.
