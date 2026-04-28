![Language](https://img.shields.io/badge/Language-中文-blue)

# 博客系统 - 全栈应用

一个基于 FastAPI 后端和 Vue 前端的完整博客系统。

---

## 🌐 Language / 语言

| English | 中文 |
|---------|------|
| [切换到英文](README.md) | ✅ 当前 |

---

## 📋 目录

- [技术栈](#技术栈)
- [前置要求](#前置要求)
- [项目结构](#项目结构)
- [安装说明](#安装说明)
- [运行应用](#运行应用)
- [API 文档](#api-文档)
- [功能特性](#功能特性)
- [API 接口](#api-接口)

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

## 前置要求

1. **Python 3.10+** 并安装 uv
2. **Node.js 18+** 并安装 npm/yarn/pnpm
3. **PostgreSQL 14+**

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

## API 文档

在 `http://localhost:8000/docs` 访问 Swagger UI

---

## 默认管理员账户

- **邮箱**: admin@example.com
- **密码**: admin123

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

---

🔄 [切换到英文 README](README.md)
