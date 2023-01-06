from django.contrib import admin
from .models import User, ToDo

admin.site.register(User)
admin.site.register(ToDo)