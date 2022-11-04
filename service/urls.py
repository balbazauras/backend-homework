
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import include
from .views import *
urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('<str:url>/', views.rdr, name="rdr"),
]
