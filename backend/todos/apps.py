"""Configuration for the Todo application."""

from django.apps import AppConfig


class TodosConfig(AppConfig):
    """Configuration class for the Todo application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "todos"
