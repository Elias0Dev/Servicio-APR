from django.shortcuts import render

def index(request):
    context={}
    return render(request, 'inicio/base.html',context)
# Create your views here.
