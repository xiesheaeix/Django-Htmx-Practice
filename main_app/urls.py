from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("signup/", views.SignupView.as_view(), name="signup")
]

main_app_urlpatterns = [
    path('check_username/', views.check_username, name='check-username')
]

urlpatterns += main_app_urlpatterns