
from django.contrib import admin
from .views import *
from . import views
from django.urls import path
urlpatterns = [
    path('', views.create_short, name="home"),
    path('r/<str:url>/', views.page_redirect, name="redirect"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('delete/<str:url>/', views.delete_url, name="delete"),
    path('toggle/<str:url>/', views.toggle_url, name="toggle"),
    path('datetime/<str:url>/<str:datetime>',
         views.change_expiration_time, name="datetime"),
]
