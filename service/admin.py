from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class UrlAdmin(admin.ModelAdmin):
    list_display = ('long_url', 'short_url')


admin.site.register(Url, UrlAdmin)
