from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from projects.models import Project
from tasks.models import Task

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.mobile_number = request.POST.get('mobile_number', '')
            job_title_choice = request.POST.get('job_title_choice', '')
            if job_title_choice == 'other':
                user.job_title = request.POST.get('job_title_other', '')
            else:
                user.job_title = job_title_choice
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
    

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.mobile_number = request.POST.get('mobile_number', '')

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        new_password = request.POST.get('new_password', '').strip()
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # keeps user logged in

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')

    return render(request, 'profile_edit.html', {'user': user})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'delete_account_confirm.html')
@login_required
def member_list(request):
    if request.user.role != 'admin':
        return redirect('dashboard')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    members = User.objects.filter(role='member')
    return render(request, 'member_list.html', {'members': members})

@login_required
def member_detail(request, member_id):
    if request.user.role != 'admin':
        return redirect('dashboard')
    from django.contrib.auth import get_user_model
    User = get_user_model()
    member = User.objects.get(id=member_id)
    member_projects = Project.objects.filter(members=member)
    member_tasks = Task.objects.filter(assigned_to=member)
    return render(request, 'member_detail.html', {
        'member': member,
        'member_projects': member_projects,
        'member_tasks': member_tasks,
    })