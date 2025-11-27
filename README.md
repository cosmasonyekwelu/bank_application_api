# Bank Application API

A secure banking backend built with Django, Django REST Framework (DRF), and JSON Web Token (JWT) authentication.
This API handles user management, authentication, account creation, and prepares the foundation for banking operations such as deposits, withdrawals, and transfers.

---

## Table of Contents

1. Project Overview
2. Features
3. Technologies Used
4. Installation
5. Environment Setup
6. Project Structure
7. Custom User Model
8. Authentication (JWT)
9. API Endpoints
10. Running Migrations
11. Creating a Superuser
12. Testing Authentication
13. Next Steps / Expansion

---

## 1. Project Overview

The Bank Application API is a backend service that provides secure account management for banking operations.
It includes a custom user model, JWT authentication, and a scalable foundation to build financial features.

The system replaces Django's username-based authentication with a fully email-based login system and enforces unique identifiers such as BVN, NIN, and bank account numbers.

---

## 2. Features

- Custom User Model (email login, no username)
- Unique BVN, NIN, and account number validation
- Custom User Manager for superuser and standard user creation
- JWT authentication (login and token refresh)
- DRF-based API configuration
- Secure endpoints using authentication classes
- Migrations and admin support

---

## 3. Technologies Used

- Python 3
- Django 5
- Django REST Framework
- Django REST Framework SimpleJWT
- SQLite (default) or PostgreSQL
- Virtual environment (venv)

---

## 4. Installation

Clone the project:

```bash
git clone <https://github.com/cosmasonyekwelu/bank_application_api>
cd mibank
```

Install requirements (after activating virtual environment):

```bash
pip install -r requirements.txt
```

If requirements.txt does not exist, install manually using:

```bash
pip install django djangorestframework djangorestframework-simplejwt
```

---

## 5. Environment Setup

Create and activate a virtual environment:

```bash
py -m venv venv
venv\Scripts\activate
```

Start the Django project (already done in this project):

```bash
django-admin startproject mibank .
```

Create the users app:

```bash
py manage.py startapp users
```

---

## 6. Project Structure

```
mibank/
│
├── mibank/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── users/
│   ├── models.py
│   ├── managers.py
│   ├── admin.py
│   ├── apps.py
│
├── db.sqlite3
├── manage.py
├── requirements.txt
```

---

## 7. Custom User Model

The system uses an email-only authentication model with no username.
Additional banking fields such as BVN, NIN, phone number, and account details are included.

### users/models.py

```python
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.core.validators import MinLengthValidator
from .managers import Manager

class User(AbstractUser, PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = (
        ("current", "Current"),
        ("savings", "Savings"),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    username = None

    bvn = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11)],
        unique=True
    )

    nin = models.CharField(
        max_length=11,
        validators=[MinLengthValidator(11)],
        unique=True
    )

    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)

    account_number = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10)],
        unique=True
    )

    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
    amount = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = Manager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Users"
```

---

## 8. Custom User Manager

### users/managers.py

```python
from django.contrib.auth.models import BaseUserManager

class Manager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)
```

---

## 9. Authentication (JWT)

Install SimpleJWT:

```bash
pip install djangorestframework-simplejwt
```

Add to INSTALLED_APPS and configure DRF:

### mibank/settings.py

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "rest_framework",
    "rest_framework_simplejwt",
]
```

### REST Framework Authentication

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ]
}
```

### SimpleJWT Configuration

```python
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
```

---

## 10. JWT URL Endpoints

### mibank/urls.py

```python
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
```

---

## 11. Running Migrations

Run database migrations:

```bash
py manage.py makemigrations
py manage.py migrate
```

---

## 12. Creating a Superuser

```bash
py manage.py createsuperuser
```

You will only provide:

- Email
- Password

---

## 13. Testing Authentication

### Obtain access and refresh tokens

POST to:

```
POST /api/token/
```

Body:

```json
{
  "email": "admin@example.com",
  "password": "yourpassword"
}
```

### Refresh access token

```
POST /api/token/refresh/
```

Body:

```json
{
  "refresh": "your_refresh_token_here"
}
```

---

## 14. Next Steps / Expansion

The API is now set up for building core banking features.
Suggested next features include:

1. User Registration Endpoint
2. Login endpoint returning JWT
3. Bank account model and linking it to user
4. Deposit, withdrawal, and transfer APIs
5. Transaction history model
6. Permissions to allow users to access only their data
7. Admin dashboard improvements
8. API documentation using DRF-YASG or Swagger

---
