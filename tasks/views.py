from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

# Create your views here.

def homepage(request):
    return render(request, 'home_page.html')

def consulta(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            tasks = Task.objects.filter(completedate__isnull=True)
            return render(request, 'consulta.html', {'tasks': tasks})
        else:
            tasks = Task.objects.filter(user = request.user, completedate__isnull=True)
            return render(request, 'consulta.html', {'tasks': tasks})
    else:
        tasks = Task.objects.filter(completedate__isnull=True)
        return render(request, 'consulta.html', {'tasks': tasks})
        
def log_in(request):
    template = "login.html"
    return render(request, template)

def singup(request):

    if request.method == 'GET':
        return render(request, 'singup.html' , {
            'form': UserCreationForm})
    else:
        print('Getting Data')
        if request.POST['password1'] == request.POST['password2']:
            try:
                #aqui se registra el usuario
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], first_name=request.POST['first_name'], last_name=request.POST['last_name'] ,email=request.POST['email'])
                user.save()
                login(request, user)
                return redirect('consulta')


            except IntegrityError:
                return render(request, 'singup.html' , {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'})


        return render(request, 'singup.html' , {
            'form': UserCreationForm,
            'error': 'Contraseña no coincide'})

def signout (request):
    logout (request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request, user)
            return redirect('home')
        

def createTask(request):
    if request.method == 'GET':
        return render(request, 'createTask.html', {
            'forms': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('consulta')
        except ValueError:
            return render(request, 'createTask.html', {
            'forms': TaskForm,
            'error': 'Datos no validos, debes iniciar sesion'
            })
        
def detalles_de_tareas(request, task_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            task = get_object_or_404(Task, pk=task_id)
            form = TaskForm(instance=task)
            return render(request, 'detalles_de_consulta.html', {'task': task, 'form': form})
        else:
            try:
                task = get_object_or_404(Task, pk=task_id)
                form = TaskForm(request.POST, instance=task)
                form.save()
                return redirect('consulta')
            except ValueError:
                return render(request, 'detalles_de_consulta.html', {'task': task, 'form': form, 'error': "Error updating task"})
    else:
        tasks = Task.objects.filter(completedate__isnull=True)
        return render(request, 'consulta.html', {'tasks': tasks, 'error':'Debes iniciar sesion'})
        
        
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.completedate = timezone.now()
        task.save()
        return redirect('consulta')
    return False
    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('consulta')
    
def consulta_completadas(request):
    tasks = Task.objects.filter(completedate__isnull = False).order_by('-completedate')
    return render(request, 'solicitudes_completadas.html', {'tasks': tasks})

@csrf_exempt
def login_api(request):
    """
    Endpoint API para login desde Angular.
    Si las credenciales son correctas, crea la sesión y devuelve a qué URL redirigir.
    """
    if request.method != 'POST':
        return JsonResponse({'detail': 'Method not allowed'}, status=405)

    # Lee JSON; si viniera como form, usa request.POST como fallback.
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    user = authenticate(request, username=username, password=password)
    if not user:
        return JsonResponse({'detail': 'Invalid credentials'}, status=401)

    # Crea la sesión (cookie) para 127.0.0.1:8000
    login(request, user)

    # URL de destino: /consulta/
    return JsonResponse({'ok': True, 'redirect': '/consulta/'}, status=200)

