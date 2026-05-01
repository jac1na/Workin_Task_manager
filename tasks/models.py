from django.db import models
from django.conf import settings
from projects.models import Project

# Create your models here.


User = settings.AUTH_USER_MODEL

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    

    def __str__(self):
        return self.title

    @property
    def completed_subtasks_count(self):
        return self.subtasks.filter(completed=True).count()

    @property
    def subtask_count(self):
        return self.subtasks.count()

class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title