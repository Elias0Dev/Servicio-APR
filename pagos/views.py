from django.shortcuts import render

def index(request):
    context={}
    return render(request, 'pagos/pagos.html',context)
# Create your views here.
