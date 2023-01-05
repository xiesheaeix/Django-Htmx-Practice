from django import forms
from django.contrib.auth.forms import UserCreationForm
from main_app.models import User


class Signup(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]