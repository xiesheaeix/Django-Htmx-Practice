from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.functions import Lower

class User(AbstractUser):
    pass

class ToDo(models.Model):
    description = models.CharField(max_length=128, unique=True)
    users = models.ManyToManyField(User, related_name='todos', through='UserTodos') #user.todos.all() to get all users 
    photo = models.ImageField(upload_to='todo_photos/', null=True, blank=True)

    class Meta: ordering =[Lower('description')]

class UserTodos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['order']