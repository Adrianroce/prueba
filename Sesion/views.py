import os

from django.shortcuts import render, redirect
from django.template import Template, Context
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages

from prueba.settings import BASE_DIR

# inicio sesion
def user_login(request):
    """Vista del login, si recibe un post (formulario)
      correcto inicia sesion con el usuario"""

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():

            username = form.cleaned_data.get('username')
            passwd = form.cleaned_data.get('password')

            usuario = authenticate(request, username=username, password=passwd)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, f"Inicio sesion correcto {username}")
                return redirect('home')
        
        form = AuthenticationForm()  # algo fue mal en el inicio de sesion
        messages.error(request, f"Falló el inicio de sesion. Parece que los datos no son correctos")
    else: 
        # solo se esta recargando la pagina
        form = AuthenticationForm()
    
    context = { 'form': form, 'title': 'LogIn YT' }
    return render(request, 'registration/login.html', context)

# registro
def user_singup(request):
    """Vista del registro de usuario, si recibe un 
    form correcto regista al usuario e inicia sesion con el mismo."""

    if request.method == "POST":

        form = UserCreationForm(request.POST)
        
        if form.is_valid():

            usuario = form.save()
            username = form.cleaned_data['username']
            login(request, usuario)
            messages.success(request, f"Bienvenido, {username}")
            return redirect('home')

        form = UserCreationForm()  # algo fue mal en el registro
        messages.error(request, f"Falló el inicio de sesion. Parece que los datos no son correctos")
    else: 

        form = UserCreationForm()
    
    context = { 'form': form, 'title': 'SinUp YT' }
    return render(request, 'registration/singup.html', context)

# cerrar sesion
def exit(request):
    """la funcion cierra la sesion del usuario"""
    
    logout(request)
    messages.success(request, f"Sesión cerrada correctamente")
    return redirect('login')

