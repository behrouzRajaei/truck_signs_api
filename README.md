# Truck Signs Backend

An online store backend built with Django and Django REST Framework for selling and customizing truck vinyl signs.
The system allows administrators to manage categories, products, lettering items, and customer orders, while exposing a REST API for frontend or external integrations.

---

## Features

- Admin panel for managing categories, products, lettering items, orders, and payments
- Customer order and payment flow integrated with Stripe
- Support for custom vinyl uploads
- Environment-specific settings (development, docker, production)
- REST API endpoints for categories, products, variations, and orders

---

## Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Python 3.8+ and PostgreSQL]

---

## Installation

1. Clone the repository:

```bash
   git clone <REPO_URL>
   cd truck_signs_api
```

2. Start the project with Docker:

First, create a Docker network (only once):

```bash
   docker network create trucknet
```

Then run PostgreSQL:

```bash
   docker run -d \
     --name postgres_db \
     --network trucknet \
     -e POSTGRES_USER=truck_user \
     -e POSTGRES_PASSWORD=truck_password \
     -e POSTGRES_DB=truck_signs_db \
     postgres:15
```

Build the Django app image:

```bash
   docker build -t truck_app .
```

Run the Django container:

```bash
   docker run -d \
     --name django_app \
     --network trucknet \
     -p 8020:8020 \
     --env-file .env \
     truck_app
```

This will automatically wait for PostgreSQL, run migrations, collect static files, and start the Django server with Gunicorn.

---

# Configuration

## Environment Variables

- The project requires a .env file for sensitive configuration values.
- A template is provided at .env.example

To create your .env:

```bash
   cp truck_signs_api/.env.example truck_signs_api/.env
```

## Minimum required variables for development:

DOCKER_SECRET_KEY=your_django_secret_key
DOCKER_DB_NAME=truck_signs_db
DOCKER_DB_USER=truck_user
DOCKER_DB_PASSWORD=truck_password
DOCKER_DB_HOST=postgres_db
DOCKER_DB_PORT=5432
DOCKER_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
DOCKER_STRIPE_SECRET_KEY=your_stripe_secret_key
DOCKER_EMAIL_HOST_USER=your_email
DOCKER_EMAIL_HOST_PASSWORD=your_email_password

---

# Security & Secrets

Never commit your real .env file to the repository.
The project already includes a .gitignore entry to keep .env private.
Use the provided .env.example file as a template — copy it to .env and replace values with your own secrets.
If you share the project, only share .env.example, not your real .env.

---

# The entrypoint.sh script runs automatically and executes:

- python manage.py migrate
- python manage.py collectstatic --noinput
- gunicorn truck_signs_designs.wsgi:application --bind 0.0.0.0:8020

---

# Running the Application

Once Docker is up:
- Django backend will be available at: http://localhost:8020
- Admin panel: http://localhost:8020/admin

To create a superuser:

```bash
   docker exec -it django_app python manage.py createsuperuser
```

Log in at:

```
http://localhost:8020/admin/
```

---

# API Endpoints

Base URL: /api/

GET /categories/ → List categories
GET /products/ → List products
GET /product-detail/<id>/ → Product details
POST /order/<id>/create/ → Create an order
POST /order-payment/<id>/ → Pay for an order (Stripe)
GET /comments/ → List comments
POST /comment/create/ → Add a new comment
POST /upload-customer-image/ → Upload a custom vinyl design

---

# evelopment Notes

- Project structure supports multiple environments (dev, docker, production)
- Static and media files served via Django in development; configure a CDN or object storage for production
- Payment flow is integrated with Stripe (test and live keys supported)

---

# Contributing

Contributions are welcome! Please fork the repo and submit pull requests.

---

# License

MIT License

This version is clean, technical, and professional — perfect for GitHub or GitLab.

---
