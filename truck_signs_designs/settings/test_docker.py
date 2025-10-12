import environ
import os
from .base import *

# Environment variables setup
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, "truck_signs_designs", "settings", ".env"))

# Basic settings
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

SECRET_KEY = env("DOCKER_SECRET_KEY")

# CORS settings
CORS_ALLOW_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:8020"]
)

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DOCKER_DB_NAME"),
        "USER": env("DOCKER_DB_USER"),
        "PASSWORD": env("DOCKER_DB_PASSWORD"),
        "HOST": env("DOCKER_DB_HOST"),
        "PORT": env("DOCKER_DB_PORT"),
    }
}

# Stripe configuration
STRIPE_PUBLISHABLE_KEY = env("DOCKER_STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = env("DOCKER_STRIPE_SECRET_KEY")

# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("DOCKER_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("DOCKER_EMAIL_HOST_PASSWORD")

# Static and media files
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

