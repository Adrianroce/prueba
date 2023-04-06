from django.urls import path

from Sesion import views
urlpatterns = [
    path('login/', views.user_login, name = "login"),
    path('accounts/login/', views.user_login, name = "login"),
    path('singup/', views.user_singup, name = "singup"),
    path('exit/', views.exit, name = "exit"),
    
]