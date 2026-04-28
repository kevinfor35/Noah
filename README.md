# Blog System - Full Stack Application

A complete blog system with FastAPI backend and Vue frontend.

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT
- **Password Hashing**: bcrypt
- **Environment Management**: uv

### Frontend
- **Framework**: Vue 3 + TypeScript
- **Router**: Vue Router 4
- **State Management**: Pinia
- **HTTP Client**: Axios
- **Build Tool**: Vite

## Prerequisites

1. **Python 3.10+** with uv installed
2. **Node.js 18+** with npm/yarn/pnpm
3. **PostgreSQL 14+**

## Project Structure

```
web/
├── backend/           # FastAPI backend
│   ├── src/
│   │   ├── routes/    # API routes
│   │   ├── config.py  # Configuration
│   │   ├── database.py # Database setup
│   │   ├── models.py  # SQLAlchemy models
│   │   ├── schemas.py # Pydantic schemas
│   │   ├── crud.py    # CRUD operations
│   │   ├── security.py # Auth utilities
│   │   └── main.py    # Application entry
│   ├── scripts/       # Database initialization
│   ├── pyproject.toml
│   └── .env           # Environment variables
└── frontend/          # Vue frontend
    ├── src/
    │   ├── views/     # Page components
    │   ├── components/# Reusable components
    │   ├── router/    # Vue Router config
    │   ├── stores/    # Pinia stores
    │   ├── api/       # API client
    │   └── types/     # TypeScript types
    ├── package.json
    └── vite.config.ts
```

## Setup Instructions

### 1. Database Setup

Create a PostgreSQL database:

```sql
CREATE DATABASE blog_db;
CREATE USER blog_user WITH PASSWORD 'blog_password';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;
```

### 2. Backend Setup

```bash
cd backend

uv sync

uv run python scripts/init_db.py
```

### 3. Frontend Setup

```bash
cd frontend

npm install
```

## Running the Application

### Start Backend

```bash
cd backend
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Start Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Documentation

Access the Swagger UI at `http://localhost:8000/docs`

## Default Admin Credentials

- **Email**: admin@example.com
- **Password**: admin123

## Features

### User Roles
- **Admin**: Full content management permissions
- **Registered User**: Read-only + interaction (like, comment)
- **Guest**: Read-only access

### Core Features
- User registration and authentication
- Blog post management (CRUD)
- Category and tag management
- Post liking (single like per user)
- Comment system
- Admin dashboard with statistics
- Search and filtering

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login` | POST | User login |
| `/api/auth/me` | GET | Get current user |
| `/api/posts` | GET/POST | List/create posts |
| `/api/posts/{id}` | GET/PUT/DELETE | Post detail/update/delete |
| `/api/categories` | GET/POST | List/create categories |
| `/api/categories/{id}` | PUT/DELETE | Update/delete category |
| `/api/tags` | GET/POST | List/create tags |
| `/api/tags/{id}` | PUT/DELETE | Update/delete tag |
| `/api/comments/post/{id}` | GET/POST | Get/post comments |
| `/api/comments/{id}` | DELETE | Delete comment |
| `/api/likes/post/{id}` | POST/GET | Like/check like |
| `/api/admin/stats` | GET | Admin statistics |
