from django.shortcuts import render

def index(request):
    context={}
    return render(request, 'inicio/index.html',context)

