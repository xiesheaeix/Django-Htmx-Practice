from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('todos/', views.TodoList.as_view(), name='todo-list'),
]

DjangoPractice_urlpatterns = [
    path('check_username/', views.check_username, name='check-username'),
    path('add-todo/', views.add_todo, name='add-todo'),
    path('delete-todo/<int:pk>/', views.delete_todo, name='delete-todo'),
    path('search-todo', views.search_todo, name='search-todo'),
    path('clear/', views.clear, name='clear'),
    path('sort/', views.sort, name='sort'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('todo-list-partial/', views.todo_partials, name='todo-list-partial'),
    path('upload-photo/<int:pk>/', views.upload_photo, name='upload-photo'),
]

urlpatterns += DjangoPractice_urlpatterns