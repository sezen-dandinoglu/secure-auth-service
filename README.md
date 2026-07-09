# 🔐 JWT Authentication API

A simple authentication API built with **FastAPI**, **PostgreSQL**, and **JWT (JSON Web Token)**.

This project demonstrates the fundamentals of backend authentication, including user registration, password hashing, login, JWT generation, and protected endpoints.

---

## 🚀 Features

- User registration
- Password hashing with bcrypt
- User login
- JWT access token generation
- Protected `/me` endpoint
- PostgreSQL integration
- Pydantic request/response validation
- Docker support

---

## 🛠 Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- Psycopg2
- Passlib (bcrypt)
- Python-JOSE (JWT)
- Pydantic
- Docker

---

## 📁 Project Structure

```
.
├── app.py              # FastAPI endpoints
├── database.py         # PostgreSQL operations
├── security.py         # Password hashing & verification
├── schemas.py          # Pydantic request/response schemas
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 📌 API Endpoints

### Register

```
POST /register
```

Creates a new user.

Example request

```json
{
    "email": "john@example.com",
    "password": "123456"
}
```

---

### Login

```
POST /login
```

Validates credentials and returns a JWT access token.

Example response

```json
{
    "access_token": "eyJhbGc...",
    "token_type": "bearer"
}
```

---

### Current User

```
GET /me
```

Returns the authenticated user's information.

Requires:

```
Authorization: Bearer <access_token>
```

---

## 🔐 Authentication Flow

```
Register
    │
    ▼
Password Hashing
    │
    ▼
Store User in PostgreSQL
    │
    ▼
Login
    │
    ▼
Verify Password
    │
    ▼
Generate JWT Token
    │
    ▼
Client Stores Token
    │
    ▼
Protected Endpoints (/me)
```

---

## 🗄 Database

Users table

| Column | Type |
|----------|-----------|
| id | SERIAL PRIMARY KEY |
| email | VARCHAR(100) UNIQUE |
| password_hash | VARCHAR(500) |
| created_at | TIMESTAMP |

Passwords are **never stored in plain text**.

---

## ▶️ Running Locally

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the API

```bash
uvicorn app:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🐳 Docker

Build

```bash
docker build -t jwt-auth-api .
```

Run

```bash
docker run -p 8000:8000 jwt-auth-api
```

---

## 📚 What I Learned

This project helped me practice:

- REST API development with FastAPI
- PostgreSQL CRUD operations
- Password hashing using bcrypt
- JWT authentication
- Request & response validation using Pydantic
- Environment variable management
- Docker basics
- Backend authentication flow

---

## 📄 License

This project is for learning and portfolio purposes.
