"""Test settings configuration for Django application."""

import os

import dj_database_url

from .base import *  # noqa: F403, F401

# Use PostgreSQL for testing
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/todos_test")
    )
}

# Disable password hashing to speed up tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Disable DEBUG mode in tests
DEBUG = False

# Use a faster test runner
TEST_RUNNER = "django.test.runner.DiscoverRunner"

# Add ROOT_URLCONF
ROOT_URLCONF = "backend.urls"

# Required applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "todos",
]
