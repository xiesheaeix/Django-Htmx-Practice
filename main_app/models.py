from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class ToDo(models.Model):
    description = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(User, related_name='todos') #user.todos.all() to get all users films