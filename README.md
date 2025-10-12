# Truck Signs Backend

An online store backend built with Django and Django REST Framework for selling and customizing truck vinyl signs.
The system allows administrators to manage categories, products, lettering items, and customer orders, while exposing a REST API for frontend or external integrations.

# Table of Contents

1. Features
2. Prerequisites
3. Installation
4. Usage
5. Security & Secrets
6. The entrypoint.sh script runs automatically and executes
7. API Endpoints
8. Contributing
9. License

# Instructure

#1. Features

- Admin panel for managing categories, products, lettering items, orders, and payments
- Customer order and payment flow integrated with Stripe
- Support for custom vinyl uploads
- Environment-specific settings (development, docker, production)
- REST API endpoints for categories, products, variations, and orders

#2. Prerequisites

- [Docker](https://docs.docker.com/get-docker/)

#3. Installation

- Clone the repository:

```bash
git clone <https://github.com/behrouzRajaei/truck_signs_api.git>
cd truck_signs_api
```

- Start the project with Docker:

a) First, create a Docker network (only once):

```bash
docker network create trucknet
```

b) Then run PostgreSQL:

```bash
docker run -d \
--name postgres_db \
--network trucknet \
-e POSTGRES_USER=truck_user \
-e POSTGRES_PASSWORD=truck_password \
-e POSTGRES_DB=truck_signs_db \
postgres:15
```

c) Build the Django app image:

```bash
docker build -t truck_app .
```

d) Run the Django container:

```bash
docker run -d \
--name django_app \
--network trucknet \
-p 8020:8020 \
--env-file .env \
truck_app
```

e) Running the Application

Once Docker is up:
- Django backend will be available at: http://localhost:8020
- Admin panel: http://localhost:8020/admin

f) create a superuser:

```bash
docker exec -it django_app python manage.py createsuperuser
```

g) Log in at:

```
http://localhost:8020/admin/
```

This will automatically wait for PostgreSQL, run migrations, collect static files, and start the Django server with Gunicorn.


#4. Usage

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


#5. Security & Secrets

Never commit your real .env file to the repository.
The project already includes a .gitignore entry to keep .env private.
Use the provided .env.example file as a template — copy it to .env and replace values with your own secrets.
If you share the project, only share .env.example, not your real .env.


#6. The entrypoint.sh script runs automatically and executes:

- python manage.py migrate
- python manage.py collectstatic --noinput
- gunicorn truck_signs_designs.wsgi:application --bind 0.0.0.0:8020


#7. API Endpoints

The base Address is: URL:8020/api/
For show the Category List: URL:8020/api/categories/
For show the Product List: URL:8020/api/products/
For show the Comments: URL:8020/api/comments/


#8. Contributing

Contributions are welcome! Please fork the repo and submit pull requests.


#9. License

MIT License

This version is clean, technical, and professional — perfect for GitHub or GitLab.

