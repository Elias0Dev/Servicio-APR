from django.shortcuts import render

def index(request):
    context={}
    return render(request, 'avisos/avisos.html',context)

# Create your views here.
