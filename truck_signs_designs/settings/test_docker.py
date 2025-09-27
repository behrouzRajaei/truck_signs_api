import environ
import os
from .base import *

# ------------------
# Basic settings
# ------------------
DEBUG = True
ALLOWED_HOSTS = ["*"]  # Replace "*" with your server's public IP if needed

# ------------------
# Environment variables
# ------------------
env = environ.Env()
# Read .env file from settings folder
environ.Env.read_env(os.path.join(BASE_DIR, "truck_signs_designs", "settings", ".env"))

SECRET_KEY = env("DOCKER_SECRET_KEY")

# ------------------
# CORS
# ------------------
CORS_ALLOW_ALL_ORIGINS = True

# ------------------
# Database
# ------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DOCKER_DB_NAME'),
        'USER': env('DOCKER_DB_USER'),
        'PASSWORD': env('DOCKER_DB_PASSWORD'),
        'HOST': env('DOCKER_DB_HOST'),
        'PORT': env('DOCKER_DB_PORT'),
    }
}

# ------------------
# Stripe keys
# ------------------
STRIPE_PUBLISHABLE_KEY = env("DOCKER_STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("DOCKER_STRIPE_SECRET_KEY")

# ------------------
# Email configuration
# ------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("DOCKER_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DOCKER_EMAIL_HOST_PASSWORD")

# ------------------
# Static and media files
# ------------------
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

