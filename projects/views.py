from django.shortcuts import render, redirect
from .models import Project
from tasks.models import Task, SubTask
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from datetime import datetime
# Create your views here.
User = get_user_model()
@login_required
def project_list(request):
    user = request.user

    # SHOW PROJECTS
    projects = Project.objects.filter(members=user)

    users = User.objects.all()

    if request.method == 'POST':

        action = request.POST.get('action')

        # 🟢 CREATE PROJECT
        if action == 'create' and user.role == 'admin':
            name = request.POST['name']
            description = request.POST['description']
            due_date = request.POST['due_date']
            members = request.POST.getlist('members')

            project = Project.objects.create(
                name=name,
                description=description,
                created_by=user,
                due_date=due_date
            )

            project.members.set(members)

        # 🟡 EDIT PROJECT
        elif action == 'edit' and user.role == 'admin':
            project = Project.objects.get(id=request.POST['project_id'])

            project.name = request.POST['name']
            project.description = request.POST['description']
            project.due_date = request.POST['due_date']

            members = request.POST.getlist('members')
            project.members.set(members)

            project.save()

        # 🔴 DELETE PROJECT
        elif action == 'delete' and user.role == 'admin':
            project = Project.objects.get(id=request.POST['project_id'])
            project.delete()

        return redirect('projects')

    return render(request, 'projects.html', {
        'projects': projects,
        'users': users,
        'page_title': 'My Projects'
    })

@login_required
def view_projects(request):
    user = request.user
    if user.role == 'admin':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(members=user)

    users = User.objects.all()
    return render(request, 'projects.html', {
        'projects': projects,
        'users': users,
        'page_title': 'View Projects'
    })

@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)

    # SECURITY: only project members or admin
    if request.user.role != 'admin' and request.user not in project.members.all():
        return redirect('projects')

    tasks = Task.objects.filter(project=project)

    users = User.objects.filter(projects=project) | User.objects.filter(role='admin')

    # CREATE TASK (ONLY INSIDE PROJECT)
    if request.method == 'POST' and request.POST.get('action') == 'create_task':

        if request.user.role == 'admin':
            due_date_str = request.POST.get('due_date', '').strip()
            assigned_to_id = request.POST.get('assigned_to')

            if due_date_str and assigned_to_id:
                try:
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                    if project.due_date and due_date > project.due_date:
                        messages.error(request, 'Task due date cannot exceed project due date.')
                    else:
                        assigned_to = users.filter(id=assigned_to_id).first()
                        if assigned_to:
                            Task.objects.create(
                                title=request.POST['title'],
                                description=request.POST['description'],
                                status='pending',
                                due_date=due_date,
                                project=project,
                                assigned_to=assigned_to
                            )
                except ValueError:
                    messages.error(request, 'Invalid due date format.')

        return redirect('project_detail', project_id=project.id)

    # CREATE SUBTASK
    if request.method == 'POST' and request.POST.get('action') == 'create_subtask':
        task = Task.objects.get(id=request.POST['task_id'])
        if request.user == task.assigned_to or request.user.role == 'admin':
            title = request.POST.get('title', '').strip()
            if title:
                SubTask.objects.create(task=task, title=title)
        return redirect('project_detail', project_id=project.id)

    # UPDATE SUBTASK
    if request.method == 'POST' and request.POST.get('action') == 'update_subtask':
        subtask = SubTask.objects.get(id=request.POST['subtask_id'])
        if request.user == subtask.task.assigned_to or request.user.role == 'admin':
            subtask.completed = request.POST.get('completed') == 'true'
            subtask.save()
        return redirect('project_detail', project_id=project.id)

    # UPDATE TASK
    if request.method == 'POST' and request.POST.get('action') == 'update_task':

        task = Task.objects.get(id=request.POST['task_id'])

        if request.user == task.assigned_to or request.user.role == 'admin':
            task.status = request.POST['status']
            task.save()

        return redirect('project_detail', project_id=project.id)

    # DELETE TASK
    if request.method == 'POST' and request.POST.get('action') == 'delete_task':

        task = Task.objects.get(id=request.POST['task_id'])

        if request.user.role == 'admin':
            task.delete()

        return redirect('project_detail', project_id=project.id)

    return render(request, 'project_detail.html', {
        'project': project,
        'tasks': tasks,
        'users': users
    })