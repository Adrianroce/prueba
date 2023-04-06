from django.urls import path

from Gestion import views
urlpatterns = [
    path('', views.home, name = "home"),
]