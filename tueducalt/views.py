from django.shortcuts import render, redirect
from django.http import HttpResponse
from marketcourses import models
import requests
import json
from . import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from marketcourses.forms import LoginForm
from marketcourses.forms import SignupForm, UserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
def campus(request):
    response = requests.get(settings.api_base_url + 'estudiantes/')
    estudiantes = response.json()
    contexto = {"estudiantes":estudiantes}
    return render(request, 'campus.html', contexto)

@unauthenticated_user
def login_campus(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("campus") 
        else:
            messages.info(request, 'Username o Password Incorrecto')

    context = {}
    return render(request, "registration/login.html", context)

def logout_campus(request):
    logout(request)
    return redirect("login")

@unauthenticated_user
def register(request):
    if request.user.is_authenticated:
        return redirect("campus")
    else:        
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                group = Group.objects.get(name="customer")
                
                user.groups.add(group)
                messages.success(request, "Cuenta creada por ... " + username)
                models.Estudiantes.objects.create(user = user, nombre = username, mail = email)
                return redirect("login")
            else:
                return HttpResponse("Escribir lógica por si ya hay usuarios con ese username o email")
        else:
            form = UserForm()  # Asignar un valor inicial a 'form'
            context = {'form': form}
            
        return render(request, "registration/signup.html", context)

def signup(request):
    url_api = settings.api_base_url + 'estudiantes/'
    response = requests.get(url_api)
    estudiantes = response.json()
    
    if request.method == 'POST':
        print("enviando 1")
        print(request.POST)
        
        form = SignupForm(request.POST)
        img = request.FILES['imagen']

        print("esta es la img: " + str(img))
        print("enviando 2")

        if form.is_valid():
            print("paso el if")
            data = json.dumps(form.cleaned_data)
            #/marketcourses/static/marketcourses/img/
            img = request.FILES['imagen']
            print("esta es la img que estoy enviando")
            print(img)
            data = form.cleaned_data
            files = {'imagen': img}  # Agregar la imagen como archivo en el diccionario 'files'
            response = requests.post(url_api, data=data, files=files)
            print("enviando")
        else:
            return HttpResponse(f"{form.errors}")
        
        if response.status_code == 201:
            return HttpResponse("Usuario creado")
        else:
            return HttpResponse(f"Error al crear usuario {response.status_code} ")
    else:
        form = SignupForm()

    contexto = {"estudiantes":estudiantes, "form":form}
    return render(request, 'registration/signup_2.html', contexto)

@allowed_users(allowed_roles = ["admin"])
def home(request):
    response = requests.get(settings.api_base_url + 'cursos/')
    productos = response.json()
  
    logo_response = requests.get(settings.api_base_url + 'files/')
    logo = logo_response.json()[0]

    cat_response = requests.get(settings.api_base_url + 'category_list/')
    categorias = cat_response.json()

    estudiantes_response = requests.get(settings.api_base_url + 'estudiantes/')
    estudiantes = estudiantes_response.json()


    lista = []
    for i in categorias:
        if i["name"] != "Cursos En Vivo":
            lista.append(i["name"])
    
    productos_complement = [producto for producto in productos if producto['category'] != 14]
    productos = [producto for producto in productos if producto['category'] == 14]

    contexto = {'productos': productos, 'logo': logo, 'categorias': lista, "productos_complement":productos_complement, "estudiantes":estudiantes} 

    return render(request, 'index.html', contexto)

#login - logout - TOkens 

# def login_user(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)

#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password = cd['password'])

#         if user is not None:
#             login(request, user)
#             print("LOGIGIGIG")
#             return HttpResponse("Authentication was succesful")
#         else:
#             return HttpResponse("Authentication failed. ")
#     else:
#          form = LoginForm()
#          print("El form LOGIN")

#     return render(request, 'login.html', {'form':form})