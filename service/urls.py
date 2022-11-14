
from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('r/<str:short_url>/', views.page_redirect, name="redirect"),
    path('delete/<str:short_url>/', views.delete_url, name="delete"),
    path('toggle/<str:short_url>/', views.toggle_url, name="toggle"),
    path('datetime/<str:short_url>/',
         views.change_expiration_time, name="datetime"),
    path('info/<str:short_url>/', views.info_page, name="info"),


]
