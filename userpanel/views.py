from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

def userpanel(request):
    return render(request, 'userpanel/userpanel.html')