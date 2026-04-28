![Language](https://img.shields.io/badge/Language-English%20%7C%20中文-blue)

# Blog System - Full Stack Application

A complete blog system with FastAPI backend and Vue frontend.

---

## 博客系统 - 全栈应用

一个基于 FastAPI 后端和 Vue 前端的完整博客系统。

---

## 📋 Table of Contents / 目录

| English | 中文 |
|---------|------|
| [Tech Stack](#tech-stack) | [技术栈](#tech-stack) |
| [Prerequisites](#prerequisites) | [前置要求](#prerequisites) |
| [Project Structure](#project-structure) | [项目结构](#project-structure) |
| [Setup Instructions](#setup-instructions) | [安装说明](#setup-instructions) |
| [Running the Application](#running-the-application) | [运行应用](#running-the-application) |
| [API Documentation](#api-documentation) | [API 文档](#api-documentation) |
| [Features](#features) | [功能特性](#features) |
| [API Endpoints](#api-endpoints) | [API 接口](#api-endpoints) |

---

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

---

## 技术栈

### 后端
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT
- **密码加密**: bcrypt
- **环境管理**: uv

### 前端
- **框架**: Vue 3 + TypeScript
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP 客户端**: Axios
- **构建工具**: Vite

---

## Prerequisites

1. **Python 3.10+** with uv installed
2. **Node.js 18+** with npm/yarn/pnpm
3. **PostgreSQL 14+**

---

## 前置要求

1. **Python 3.10+** 并安装 uv
2. **Node.js 18+** 并安装 npm/yarn/pnpm
3. **PostgreSQL 14+**

---

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

---

## 项目结构

```
web/
├── backend/           # FastAPI 后端
│   ├── src/
│   │   ├── routes/    # API 路由
│   │   ├── config.py  # 配置文件
│   │   ├── database.py # 数据库设置
│   │   ├── models.py  # SQLAlchemy 模型
│   │   ├── schemas.py # Pydantic 模式
│   │   ├── crud.py    # CRUD 操作
│   │   ├── security.py # 认证工具
│   │   └── main.py    # 应用入口
│   ├── scripts/       # 数据库初始化
│   ├── pyproject.toml
│   └── .env           # 环境变量
└── frontend/          # Vue 前端
    ├── src/
    │   ├── views/     # 页面组件
    │   ├── components/# 可复用组件
    │   ├── router/    # Vue Router 配置
    │   ├── stores/    # Pinia 状态管理
    │   ├── api/       # API 客户端
    │   └── types/     # TypeScript 类型
    ├── package.json
    └── vite.config.ts
```

---

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

---

## 安装说明

### 1. 数据库设置

创建 PostgreSQL 数据库：

```sql
CREATE DATABASE blog_db;
CREATE USER blog_user WITH PASSWORD 'blog_password';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;
```

### 2. 后端设置

```bash
cd backend

uv sync

uv run python scripts/init_db.py
```

### 3. 前端设置

```bash
cd frontend

npm install
```

---

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

---

## 运行应用

### 启动后端

```bash
cd backend
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API 服务将在 `http://localhost:8000` 运行

### 启动前端

```bash
cd frontend
npm run dev
```

前端服务将在 `http://localhost:5173` 运行

---

## API Documentation

Access the Swagger UI at `http://localhost:8000/docs`

---

## API 文档

在 `http://localhost:8000/docs` 访问 Swagger UI

---

## Default Admin Credentials

- **Email**: admin@example.com
- **Password**: admin123

---

## 默认管理员账户

- **邮箱**: admin@example.com
- **密码**: admin123

---

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

---

## 功能特性

### 用户角色
- **管理员**: 完整的内容管理权限
- **注册用户**: 只读 + 互动（点赞、评论）
- **访客**: 只读访问

### 核心功能
- 用户注册和认证
- 博客文章管理（CRUD）
- 分类和标签管理
- 文章点赞（每个用户只能点赞一次）
- 评论系统
- 管理员仪表盘和统计
- 搜索和过滤

---

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

---

## API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/auth/register` | POST | 注册新用户 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/auth/me` | GET | 获取当前用户 |
| `/api/posts` | GET/POST | 列出/创建文章 |
| `/api/posts/{id}` | GET/PUT/DELETE | 文章详情/更新/删除 |
| `/api/categories` | GET/POST | 列出/创建分类 |
| `/api/categories/{id}` | PUT/DELETE | 更新/删除分类 |
| `/api/tags` | GET/POST | 列出/创建标签 |
| `/api/tags/{id}` | PUT/DELETE | 更新/删除标签 |
| `/api/comments/post/{id}` | GET/POST | 获取/发布评论 |
| `/api/comments/{id}` | DELETE | 删除评论 |
| `/api/likes/post/{id}` | POST/GET | 点赞/检查点赞 |
| `/api/admin/stats` | GET | 管理员统计 |
