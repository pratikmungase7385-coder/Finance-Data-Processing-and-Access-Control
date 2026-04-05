# Finance Data Processing and Access Control Backend

A Django REST Framework backend for a finance dashboard system with role-based access control, financial record management, and summary analytics.

---

## Tech Stack

| Layer        | Choice                        | Reason                                           |
|--------------|-------------------------------|--------------------------------------------------|
| Language     | Python 3.10+                  | Readable, widely used for backend dev            |
| Framework    | Django 4.2 + DRF 3.15        | Batteries-included, great ORM, JWT support       |
| Auth         | JWT (SimpleJWT)               | Stateless, scalable, industry standard           |
| Database     | SQLite (dev) / PostgreSQL (prod) | SQLite for zero-setup local dev; swap easily  |
| Filtering    | django-filter                 | Clean, declarative query filtering               |

---

## Project Structure

```
finance_backend/
├── manage.py
├── requirements.txt
├── finance_backend/         # Django project (settings, root URLs, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── users/                   # User management + auth + permissions
│   ├── models.py            # Custom User model with roles
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py       # Role-based permission classes
│   └── admin.py
├── records/                 # Financial records CRUD
│   ├── models.py            # FinancialRecord model
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py           # Filtering logic
│   └── management/
│       └── commands/
│           └── seed_data.py # Sample data seeder
└── dashboard/               # Analytics + summary APIs
    ├── views.py
    └── urls.py
```

---

## Setup & Installation

### 1. Clone and create virtual environment

```bash
git clone <repo-url>
cd finance_backend

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Seed sample data (optional but recommended)

```bash
python manage.py seed_data
```

This creates 3 test users and 15 sample financial records.

| Role    | Email                  | Password     |
|---------|------------------------|--------------|
| Admin   | admin@finance.com      | admin@123    |
| Analyst | analyst@finance.com    | analyst@123  |
| Viewer  | viewer@finance.com     | viewer@123   |

### 5. Start the server

```bash
python manage.py runserver
```

Server runs at: `http://127.0.0.1:8000`

---

## Authentication

All protected endpoints require a **Bearer JWT token** in the `Authorization` header.

```
Authorization: Bearer <access_token>
```

### Login

```
POST /api/auth/login/
Content-Type: application/json

{
  "email": "admin@finance.com",
  "password": "admin@123"
}
```

**Response:**
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>",
  "user": {
    "id": 1,
    "email": "admin@finance.com",
    "full_name": "Admin User",
    "role": "admin",
    "is_active": true,
    "date_joined": "2026-04-05T10:00:00Z"
  }
}
```

### Refresh Token

```
POST /api/auth/refresh/
{ "refresh": "<refresh_token>" }
```

---

## Role-Based Access Control

| Action                       | Viewer | Analyst | Admin |
|------------------------------|:------:|:-------:|:-----:|
| Login                        | ✅     | ✅      | ✅    |
| View own profile             | ✅     | ✅      | ✅    |
| List financial records       | ✅     | ✅      | ✅    |
| View a record detail         | ✅     | ✅      | ✅    |
| Recent activity dashboard    | ✅     | ✅      | ✅    |
| Overview / category / trends | ❌     | ✅      | ✅    |
| Full summary dashboard       | ❌     | ✅      | ✅    |
| Create financial records     | ❌     | ❌      | ✅    |
| Update financial records     | ❌     | ❌      | ✅    |
| Delete financial records     | ❌     | ❌      | ✅    |
| Create / manage users        | ❌     | ❌      | ✅    |
| Update user role/status      | ❌     | ❌      | ✅    |
| Deactivate users             | ❌     | ❌      | ✅    |

---

## API Reference

### Auth Endpoints

| Method | URL                  | Access | Description             |
|--------|----------------------|--------|-------------------------|
| POST   | /api/auth/login/     | Public | Get JWT tokens          |
| POST   | /api/auth/refresh/   | Public | Refresh access token    |

---

### User Endpoints

| Method | URL               | Access | Description                     |
|--------|-------------------|--------|---------------------------------|
| GET    | /api/users/me/    | All    | Get own profile                 |
| GET    | /api/users/       | Admin  | List all users                  |
| POST   | /api/users/       | Admin  | Create a new user               |
| GET    | /api/users/{id}/  | Admin  | Get user by ID                  |
| PATCH  | /api/users/{id}/  | Admin  | Update user role or status      |
| DELETE | /api/users/{id}/  | Admin  | Deactivate user (soft delete)   |

#### Create User (Admin)
```json
POST /api/users/
{
  "email": "john@example.com",
  "full_name": "John Doe",
  "password": "securepass",
  "role": "analyst",
  "is_active": true
}
```
Valid roles: `viewer`, `analyst`, `admin`

#### Update User (Admin)
```json
PATCH /api/users/2/
{
  "role": "admin",
  "is_active": false
}
```

---

### Financial Record Endpoints

| Method | URL               | Access        | Description                  |
|--------|-------------------|---------------|------------------------------|
| GET    | /api/records/     | All           | List records (filterable)    |
| POST   | /api/records/     | Admin         | Create a new record          |
| GET    | /api/records/{id}/| All           | Retrieve record by ID        |
| PATCH  | /api/records/{id}/| Admin         | Update record                |
| DELETE | /api/records/{id}/| Admin         | Soft delete record           |

#### Create Record (Admin)
```json
POST /api/records/
{
  "amount": "45000.00",
  "transaction_type": "income",
  "category": "salary",
  "date": "2026-04-01",
  "description": "April salary"
}
```

Valid `transaction_type`: `income`, `expense`

Valid `category`: `salary`, `investment`, `freelance`, `rent`, `utilities`, `food`, `transport`, `healthcare`, `entertainment`, `education`, `tax`, `other`

#### Filtering Records

All filters are query parameters on `GET /api/records/`:

| Parameter          | Example              | Description               |
|--------------------|----------------------|---------------------------|
| `transaction_type` | `?transaction_type=income` | Filter by type       |
| `category`         | `?category=salary`   | Filter by category        |
| `date_from`        | `?date_from=2026-01-01` | Records on or after   |
| `date_to`          | `?date_to=2026-03-31` | Records on or before    |
| `amount_min`       | `?amount_min=1000`   | Min amount                |
| `amount_max`       | `?amount_max=50000`  | Max amount                |
| `search`           | `?search=salary`     | Search in description/category |
| `ordering`         | `?ordering=-amount`  | Sort (prefix `-` for desc)|
| `page`             | `?page=2`            | Pagination (20 per page)  |

**Combined example:**
```
GET /api/records/?transaction_type=expense&category=rent&date_from=2026-01-01&ordering=-amount
```

---

### Dashboard Endpoints

| Method | URL                              | Access          | Description                        |
|--------|----------------------------------|-----------------|------------------------------------|
| GET    | /api/dashboard/overview/         | Analyst + Admin | Total income, expense, net balance |
| GET    | /api/dashboard/category-breakdown/ | Analyst + Admin | Per-category income/expense totals |
| GET    | /api/dashboard/monthly-trends/   | Analyst + Admin | Month-by-month trends              |
| GET    | /api/dashboard/weekly-trends/    | Analyst + Admin | Week-by-week trends                |
| GET    | /api/dashboard/recent-activity/  | All             | Most recent N records              |
| GET    | /api/dashboard/summary/          | Analyst + Admin | Full combined summary              |

#### Overview Response
```json
{
  "total_income": 193500.00,
  "total_expenses": 70000.00,
  "net_balance": 123500.00,
  "total_records": 15
}
```

#### Monthly Trends
```
GET /api/dashboard/monthly-trends/?months=3
```
```json
{
  "months": 3,
  "trends": [
    { "month": "2026-02", "income": 78000.0, "expense": 22000.0, "net": 56000.0 },
    { "month": "2026-03", "income": 85000.0, "expense": 25000.0, "net": 60000.0 }
  ]
}
```

#### Recent Activity
```
GET /api/dashboard/recent-activity/?limit=5
```

---

## Error Handling

All errors return a structured JSON response with appropriate HTTP status codes.

| Code | Meaning                     | Example Scenario                    |
|------|-----------------------------|-------------------------------------|
| 400  | Bad Request / Validation    | Missing required field, invalid value |
| 401  | Unauthorized                | Missing or invalid JWT token        |
| 403  | Forbidden                   | Role does not have permission       |
| 404  | Not Found                   | Record/User ID does not exist       |
| 405  | Method Not Allowed          | Wrong HTTP verb on endpoint         |

**Validation error example:**
```json
{
  "amount": ["Amount must be greater than zero."],
  "transaction_type": ["transaction_type must be one of: income, expense"]
}
```

**Auth error example:**
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

---

## Design Decisions & Assumptions

### 1. Custom User Model
Used `AbstractBaseUser` instead of Django's default `User` to make email the login identifier. This is the recommended pattern for production Django apps and avoids painful migrations later.

### 2. Soft Deletes
Both users and financial records are never hard-deleted. Users are marked `is_active=False`, records get `is_deleted=True`. This preserves audit history — important for financial data.

### 3. Role Enforcement via Permission Classes
Permissions are enforced using dedicated DRF `BasePermission` subclasses (`IsAdmin`, `IsAnalystOrAdmin`, `IsAnyRole`, `IsAdminOrReadOnly`) rather than inline `if` checks. This keeps views clean and makes the access rules easy to audit in one place.

### 4. Dashboard Access Differentiation
`/api/dashboard/recent-activity/` is accessible to **all roles** including Viewer, so they can at least see what's happening. All analytical/aggregate endpoints (trends, overview, breakdown) are restricted to Analyst+Admin.

### 5. SQLite for Simplicity
SQLite requires zero configuration and is ideal for local development and assessment. To switch to PostgreSQL, only the `DATABASES` setting needs to change — the rest of the code is DB-agnostic via Django ORM.

### 6. Pagination
Default page size is 20. Clients can use `?page=N` to navigate. This prevents large payloads on record lists.

### 7. Amount Validation
Amounts are always stored as positive `DecimalField(max_digits=14, decimal_places=2)`. The `transaction_type` field (`income` / `expense`) determines the direction. This avoids confusion from negative values.

---

## Running Django Admin

```bash
python manage.py createsuperuser
# Then visit: http://127.0.0.1:8000/admin/
```

The admin panel provides a GUI to inspect and manage users and records directly.
