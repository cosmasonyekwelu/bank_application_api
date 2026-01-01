
# Bank Application API

A secure banking backend built with **Django**, **Django REST Framework (DRF)**, and **JWT authentication**.
This API supports user authentication, account management, transactions, loan applications, API documentation, and production deployment on Render.

---

## Table of Contents

1. Project Overview
2. Features
3. Technologies Used
4. Installation
5. Environment Setup
6. Project Structure
7. Authentication (JWT)
8. Accounts & Transactions
9. Loan Applications & Permissions
10. API Documentation (Swagger)
11. Admin Configuration
12. Database Migrations
13. Deployment to Render
14. Common Issues & Fixes
15. Next Steps

---

## 1. Project Overview

The Bank Application API simulates real-world banking backend operations.
It replaces Django’s default username-based authentication with **email-based login**, supports **bank accounts**, **financial transactions**, and **loan applications**, and enforces business rules using **custom permissions**.

The system is designed with scalability, security, and production deployment in mind.

---

## 2. Features

* Email-based authentication (no username)
* JWT authentication (access & refresh tokens)
* User profile updates
* One-to-one User ↔ Account relationship
* Savings and Current account types
* Deposits and transfers
* Transaction history (sender → receiver)
* Loan application system (current accounts only)
* Custom permission classes
* Swagger / OpenAPI documentation
* Django Admin integration
* PostgreSQL-ready deployment
* Hosted on Render

---

## 3. Technologies Used

* Python 3
* Django 5
* Django REST Framework
* SimpleJWT
* drf-spectacular (Swagger/OpenAPI)
* PostgreSQL (production)
* SQLite (local development)
* Gunicorn
* Render

---

## 4. Installation

Clone the repository:

```bash
git clone https://github.com/cosmasonyekwelu/bank_application_api
cd bank_application_api
```

Create and activate a virtual environment:

```bash
py -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 5. Environment Setup

### Local `.env` file (do not commit)

```env
DEBUG=True
SECRET_KEY=django-insecure-local-key
DATABASE_URL=sqlite:///db.sqlite3
```

Add `.env` to `.gitignore`.

In `settings.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 6. Project Structure

```
bank_application_api/
│
├── mibank/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│
├── users/
├── accounts/
├── transactions/
│
├── manage.py
├── Procfile
├── requirements.txt
```

---

## 7. Authentication (JWT)

JWT authentication is handled using **SimpleJWT**.

### DRF Configuration

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

### Login Endpoint

```
POST /auth/login/
```

Request:

```json
{
  "email": "loan@test.com",
  "password": "StrongPass123!"
}
```

Response:

```json
{
  "message": "User Login successful",
  "access": "JWT_ACCESS_TOKEN",
  "refresh": "JWT_REFRESH_TOKEN"
}
```

---

## 8. Accounts & Transactions

### Accounts

* One account per user
* Account types: savings, current
* Auto-generated 10-digit account number
* Balance tracking

### Transactions

A **self-referential model** is used:

* sender → Accounts
* receiver → Accounts

This supports:

* Deposits (sender = receiver)
* Transfers (sender ≠ receiver)

---

## 9. Loan Applications & Permissions

### LoanApplications Model

```python
class LoanApplications(models.Model):
    user = models.ForeignKey("accounts.Accounts", on_delete=models.CASCADE)
    principal_amount = models.FloatField()
    is_approved = models.BooleanField(default=False)
```

### Custom Permission

Only **current accounts** can apply for loans.

```python
class IscurrentAccount(BasePermission):
    def has_permission(self, request, view):
        account = Accounts.objects.get(user=request.user.id)
        return account.account_type == "current"
```

### Apply for Loan

```
POST /transactions/loan/
```

Request:

```json
{
  "principal_amount": 50000
}
```

Response:

```json
{
  "message": "Loan application submitted successfully"
}
```

---

## 10. API Documentation (Swagger)

Swagger documentation is generated using **drf-spectacular**.

### Available at:

```
/api/docs/swagger/
```

We documented the **login endpoint** using `extend_schema`, including:

* Summary
* Description
* Request example
* Response example

This allows browser-based testing without Postman.

---

## 11. Admin Configuration

Transactions and loans are registered in Django admin.

```python
admin.site.register(Transactions)
admin.site.register(LoanApplications)
```

Admins can:

* View all transactions
* Review loan applications
* Approve or reject loans (future enhancement)

---

## 12. Database Migrations

Run migrations locally:

```bash
py manage.py makemigrations
py manage.py migrate
```

Create admin user:

```bash
py manage.py createsuperuser
```

---

## 13. Deployment to Render

### Procfile

At project root:

```procfile
web: gunicorn mibank.wsgi
```

This follows Django and Gunicorn documentation.
Gunicorn automatically detects the `application` callable.

---

### Render Environment Variables

Set in Render Dashboard:

| Key           | Value                   |
| ------------- | ----------------------- |
| SECRET_KEY    | Django secret key       |
| DATABASE_URL  | PostgreSQL internal URL |
| DEBUG         | False                   |
| ALLOWED_HOSTS | your-app.onrender.com   |

---

### Deployment Steps

1. Push code to GitHub
2. Create PostgreSQL service on Render
3. Create Web Service (Python)
4. Build command:

```
pip install -r requirements.txt
```

5. Start command:

```
gunicorn mibank.wsgi
```

6. Run migrations in Render shell:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 14. Common Issues & Fixes

| Issue          | Cause              | Fix                    |
| -------------- | ------------------ | ---------------------- |
| DisallowedHost | Missing domain     | Set ALLOWED_HOSTS      |
| No such table  | Migrations not run | Run migrate            |
| App crash      | gunicorn missing   | Add to requirements    |
| Loan blocked   | Savings account    | Create current account |

---

## 15. Next Steps

Planned improvements:

1. Loan approval workflow
2. Interest calculations
3. Transaction status lifecycle
4. Rate limiting
5. Audit logging
6. Automated tests
7. CI/CD pipeline

---

## Summary

This project demonstrates:

* Real-world backend architecture
* Secure authentication
* Financial data modeling
* Permissions and business rules
* API documentation
* Production deployment

The Bank Application API is now **production-ready** and extensible.

---

