from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from projects.models import Project
from tasks.models import Task

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            return render(request, 'login.html', {
                'error': 'Username and password are required.'
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    user = request.user

    if user.role == 'admin':
        projects_count = Project.objects.count()
        tasks_count = Task.objects.count()
    else:
        projects_count = Project.objects.filter(members=user).count()
        tasks_count = Task.objects.filter(assigned_to=user).count()

    return render(request, 'dashboard.html', {
        'projects_count': projects_count,
        'tasks_count': tasks_count
    })