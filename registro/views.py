from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def registro(request):
    return render(request, 'registro/registro.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def registro(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validaciones básicas
        if not username or not email or not password1 or not password2:
            messages.error(request, "Todos los campos son obligatorios.")
        elif password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya existe.")
        else:
            # Crear el usuario
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')
    return render(request, 'registro/registro.html')
