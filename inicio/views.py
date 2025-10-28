from django.shortcuts import render

def index(request):
    context={}
    return render(request, 'inicio/inicio.html',context)

