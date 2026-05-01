from django.urls import path
from .views import project_list, project_detail, view_projects

urlpatterns = [
    path('', project_list, name='projects'),
    path('view/', view_projects, name='view_projects'),
    path('<int:project_id>/', project_detail, name='project_detail'),
]