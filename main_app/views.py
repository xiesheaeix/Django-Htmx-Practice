from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings

from main_app.models import ToDo, UserTodos
from main_app.utils import get_max_order, reorder
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
    model = UserTodos
    paginate_by = settings.PAGINATE_BY
    context_object_name = 'todos'

    def get_template_names(self):
        if self.request.htmx:
            return 'partials/todo-list-elements.html'
        return 'todos.html'

    def get_queryset(self):
      return UserTodos.objects.prefetch_related('todo').filter(user=self.request.user)


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
    if not UserTodos.objects.filter(todo=todo, user=request.user).exists():
        UserTodos.objects.create(
            todo=todo, 
            user=request.user, 
            order=get_max_order(request.user)
        )

    # return template w/ all the users todos
    todos = UserTodos.objects.filter(user=request.user)
    messages.success(request, f"Added {description} to list of films")
    return render(request, 'partials/todo-list.html', {'todos': todos})

@login_required
@require_http_methods(['DELETE'])
def delete_todo(request, pk):
    # remove film from users list
    UserTodos.objects.get(pk=pk).delete()
    reorder(request.user)
    todos = UserTodos.objects.filter(user=request.user)
    return render(request, 'partials/todo-list.html', {'todos': todos})

@login_required
def search_todo(request):
    search_text = request.POST.get('search')
    results = ToDo.objects.filter(description__icontains=search_text)

    #ToDo: figure out why todos are saving as all users, once more user centric you can add this 
    # user_todos = UserTodos.objects.filter(user=request.user)
    # results = ToDo.objects.filter(description__icontains=search_text).exclude(
    #     description__in=user_todos.value_list('todo__description', flat=True)
    # )

    context = {'results': results}
    return render(request, 'partials/search-results.html', context)

def clear(request):
    return HttpResponse("")

def sort(request):
    todos_pks_order = request.POST.getlist('todo_order')
    todos = []

    usertodos = UserTodos.objects.prefetch_related('todo').filter(user=request.user)
    for idx, todo_pk in enumerate(todos_pks_order, start=1):
        usertodo = next(u for u in usertodos if u.pk == todo_pk)
        usertodo.order = idx
        usertodo.save()
        todos.append(usertodo)

    paginator = Paginator(todos, settings.PAGINATE_BY)
    page_number = len(todos_pks_order) / settings.PAGINATE_BY
    page_obj = paginator.get_page(page_number)
    context = {'todos': todos, 'page_obj': page_obj}


    return render(request, 'partials/todo-list.html', context)

@login_required
def detail(request, pk):
    usertodo = get_object_or_404(UserTodos, pk=pk)
    context = {'usertodo': usertodo}
    return render(request, 'partials/todo-detail.html', context)

@login_required
def todo_partials(request):
    todos = UserTodos.objects.filter(user=request.user)
    return render(request, 'partials/todo-list.html', {'todos': todos})


@login_required
def upload_photo(request, pk):
    usertodo = get_object_or_404(UserTodos, pk=pk)
    photo = request.FILES.get('photo')
    usertodo.todo.photo.save(photo.name, photo)
    context = {'usertodo': usertodo}
    return render(request, 'partials/todo-detail.html', context)
