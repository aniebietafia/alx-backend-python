# Project Objectives
By the end of this project, learners will be able to:

* Scaffold a Django project using industry-standard project structures.
* Identify, define, and implement scalable data models using Django’s ORM.
* Establish one-to-many, many-to-many, and one-to-one relationships between models.
* Create clean and modular Django apps.
* Set up and configure URL routing for APIs using Django’s path and include functions.
* Follow best practices in file structure, code organization, and documentation.
* Build a maintainable API layer using Django REST Framework (optional enhancement).
* Validate and test APIs with real data using tools like Postman or Swagger.

# Setting Up a Django Project: A Comprehensive Guide
- ## Prerequisites
    - Python 3.x installed
    - pip package manager
    - Basic understanding of Python and web development concepts
    - Familiarity with command line interface (CLI)
    - (Optional) Virtual environment tool like venv or virtualenv
- ## Tools and Libraries
    - Django
    - Django REST Framework (for API development)
    - SQLite (default database) or PostgreSQL/MySQL for production
    - Postman or Swagger for API testing and documentation
    - Git for version control
    - (Optional) Docker for containerization
- ## Setup Instructions
1. Create a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
2. Install Django and Django REST Framework:
    ```bash
    pip install django djangorestframework
    ```
3. Install required packages for environment management:
    ```bash
    pip install -r requirements.txt
    ```
4. Database setup (if using PostgreSQL/MySQL):
    - Install the database server and client libraries
    - Configure database settings in `settings.py`
5. Make migrations and migrate:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. Create a superuser for admin access:
    ```bash
    python manage.py createsuperuser
    ```
7. Run the development server:
    ```bash
    python manage.py runserver
    ```
8. Access the admin panel at `http://127.0.0.1:8000/admin` and log in with the superuser credentials.
9. Access the docs at `http://127.0.0.1:8000/docs` (if using DRF's built-in documentation).

## Key Implementation Phases
1. Project Setup and Environment Configuration
    - Create a virtual environment
    - Install Django
    - Scaffold the project with django-admin startproject and python manage.py startapp
    - Configure settings.py (INSTALLED_APPS, middleware, CORS, etc.)

2. Defining Data Models

    - Identify core models based on requirements (e.g., User, Property, Booking)

    - Use Django ORM to define model classes

    - Add field types, constraints, and default behaviors

    - Apply migrations and use Django Admin for verification

3. Establishing Relationships

    - Implement foreign keys, many-to-many relationships, and one-to-one links

    - Use related_name, on_delete, and reverse relationships effectively

    - Use Django shell to test object relations

4. URL Routing
    - Define app-specific routes using urls.py

    - Use include() to modularize routes per app

    - Follow RESTful naming conventions: /api/properties/, /api/bookings/<id>/

    - Create nested routes when necessary

5. Best Practices and Documentation

    - Use views.py to separate logic and ensure Single Responsibility

    - Document endpoints using README or auto-generated documentation tools

    - Keep configuration settings modular (e.g., using .env or settings/ directory structure)

    - Use versioned APIs (e.g., /api/v1/) to future-proof development

## Best Practices for Scaffolding and Structuring Projects
| Area               | Best Practices                                                                                             |
|--------------------|------------------------------------------------------------------------------------------------------------|
| Project Structure  | Keep a modular structure with reusable apps, consistent naming, and organized folders (apps/, core/, etc.) |
| Environment Config | Use `.env` files and `django-environ` to manage secret keys and settings                                   |
| Models             | Avoid business logic in models; use helper functions or managers when necessary                            |
| Migrations         | Commit migration files and test them on a fresh database                                                   |
| Routing            | Namespace routes and separate admin/API/user-related URLs for clarity                                      |
| Security           | Use `ALLOWED_HOSTS`, avoid hardcoding credentials, and enable CORS properly                                |
| Testing            | Use Django’s test client or tools like Postman to validate endpoints early and often                       |
| Documentation      | Add inline comments, maintain a clear README, and use tools like Swagger or DRF’s built-in docs            |

## Settings up with Docker (Optional)
1. Build the Docker image:
    ```bash
    docker build -t messaging_app .
    ```
2. Run the Docker container:
    ```bash
    docker run -p 8000:8000 --env-file .env messaging_app
    ```
3. Access the application at `http://127.0.0.1:8000/api/`.

## Commands to run Docker Compose
1. Build and start the services:
    ```bash
    docker-compose up --build
    ```
2. Run in detached mode:
    ```bash
    docker-compose up -d
    ```
3. View logs:
    ```bash
    docker-compose logs -f
    ```
4. Stop the services:
    ```bash
    docker-compose down
    ```
5. Stop and remove containers, networks, and volumes:
    ```bash
    docker-compose down -v
    ```