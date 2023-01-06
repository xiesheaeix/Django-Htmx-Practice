from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.contrib.auth import get_user_model
from main_app.models import ToDo
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages

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

class TodoList(LoginRequiredMixin, ListView):
    template_name = 'todos.html'
    model = ToDo
    context_object_name = 'todos'

    def get_queryset(self):
        user = self.request.user
        return user.todos.all()


def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("<div id='username-error' class='error'>This username already exists</div>")
    else:
        return HttpResponse("<div id='username-error' class='success'>This username is available</div>")

@login_required
def add_todo(request):
    description = request.POST.get('todo-description')
    todo = ToDo.objects.get_or_create(description=description)[0]

    # add todo to the user's list
    request.user.todos.add(todo)

    # return template w/ all the users todos
    todos = request.user.todos.all()
    messages.success(request, f"Added {description} to list of films")
    return render(request, 'partials/todo-list.html', {'todos': todos})

@login_required
@require_http_methods(['DELETE'])
def delete_todo(request, pk):
    # remove film from users list
    request.user.todos.remove(pk)
    todos = request.user.todos.all()
    return render(request, 'partials/todo-list.html', {'todos': todos})

@login_required
def search_todo(request):
    search_text = request.POST.get('search')
    results = ToDo.objects.filter(description__icontains=search_text)

    #ToDo: figure out why todos are saving as all users, once more user centric you can add this 
    # user_todos = request.user.todos.all()
    # results = ToDo.objects.filter(description__icontains=search_text).exclude(
    #     description__in=user_todos.value_list('description', flat=True)
    # )

    context = {'results': results}
    return render(request, 'partials/search-results.html', context)

def clear(request):
    return HttpResponse("")