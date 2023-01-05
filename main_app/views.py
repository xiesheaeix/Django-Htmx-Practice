from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.contrib.auth import get_user_model

from main_app.forms import Signup

def home(request):
    return render(request, 'home.html')
    
class Login(LoginView):
    template_name = 'registration/login.html'

class SignupView(FormView):
    form_class = Signup
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)

def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div style='color: red;'>This username already exists</div>")
    else:
        return HttpResponse("<div style='color: green;'>This username is available</div>")
