from django.urls import path
from .views import task_list, view_tasks

urlpatterns = [
    path('', task_list, name='tasks'),
    path('view/', view_tasks, name='view_tasks'),
]