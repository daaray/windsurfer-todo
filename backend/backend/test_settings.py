"""
Django test settings for backend project.
"""

from .settings import *

# Use an in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Make password hashing faster in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable DEBUG mode in tests
DEBUG = False

# Use a faster test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Add ROOT_URLCONF
ROOT_URLCONF = 'backend.urls'

# Required applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'todos',
]
