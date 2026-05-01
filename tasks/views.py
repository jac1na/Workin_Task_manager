
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Task, SubTask
from projects.models import Project

User = get_user_model()

@login_required
def task_list(request):
    user = request.user

    # SHOW TASKS
    tasks = Task.objects.filter(assigned_to=user).select_related('project','assigned_to').prefetch_related('subtasks')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_subtask':
            subtask = SubTask.objects.get(id=request.POST['subtask_id'])
            if request.user == subtask.task.assigned_to or request.user.role == 'admin':
                subtask.completed = request.POST.get('completed') == 'true'
                subtask.save()
            return redirect('tasks')

        if 'task_id' in request.POST:
            task = Task.objects.get(id=request.POST['task_id'])
            if request.user == task.assigned_to:
                task.status = request.POST['status']
                task.save()
            return redirect('tasks')

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'page_title': 'My Tasks'
    })

@login_required
def view_tasks(request):
    user = request.user
    if user.role == 'admin':
        tasks = Task.objects.all().select_related('project','assigned_to').prefetch_related('subtasks')
    else:
        tasks = Task.objects.filter(project__members=user).select_related('project','assigned_to').prefetch_related('subtasks')

    projects = Project.objects.all()
    users = User.objects.filter(role='member')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_subtask':
            subtask = SubTask.objects.get(id=request.POST['subtask_id'])
            if request.user == subtask.task.assigned_to or request.user.role == 'admin':
                subtask.completed = request.POST.get('completed') == 'true'
                subtask.save()
            return redirect('view_tasks')

        if 'task_id' in request.POST:
            task = Task.objects.get(id=request.POST['task_id'])
            if request.user == task.assigned_to:
                task.status = request.POST['status']
                task.save()
            return redirect('view_tasks')

    return render(request, 'tasks.html', {
        'tasks': tasks,
        'projects': projects,
        'users': users,
        'page_title': 'View Tasks'
    })