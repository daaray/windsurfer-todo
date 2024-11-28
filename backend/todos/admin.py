"""Admin configuration for the Todo application."""

from django.contrib import admin

from .models import Todo

admin.site.register(Todo)
