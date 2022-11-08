from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UrlAdmin(admin.ModelAdmin):
    list_display = ('long', 'short')


admin.site.register(Url, UrlAdmin)
