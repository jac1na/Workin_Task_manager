from django.db import models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='projects')
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name