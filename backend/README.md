# Blog API Backend

基于 FastAPI 的博客系统后端 API。

## 功能特性

- **用户认证**: 注册、登录、JWT 令牌认证
- **博客文章**: 创建、阅读、更新、删除文章
- **分类管理**: 创建和管理文章分类
- **标签管理**: 创建和管理文章标签
- **评论系统**: 用户可以对文章发表评论
- **点赞功能**: 用户可以点赞文章
- **管理员权限**: 管理员可以管理所有内容、提升用户为管理员

## 技术栈

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (异步)
- PostgreSQL
- JWT 认证
- Uvicorn

## 快速开始

### 环境要求

- Python 3.10+
- PostgreSQL 14+
- uv (Python 包管理器)

### 安装依赖

使用 uv 安装项目依赖：

```bash
cd backend
uv install
```

### 配置环境变量

创建 `.env` 文件：

```env
DATABASE_URL=postgresql+asyncpg://blog_user:blog_password@localhost/blog_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 初始化数据库

```bash
uv run python scripts/init_db.py
```

### 启动服务

使用 uvicorn 直接启动：

```bash
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

或使用 Python 模块方式：

```bash
uv run python -m src.main
```

服务将在 `http://localhost:8000` 启动。

## API 文档

启动服务后，访问以下地址查看 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API 端点

### 认证

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 文章

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/posts/` | 获取文章列表 |
| GET | `/api/posts/{post_id}` | 获取单篇文章 |
| POST | `/api/posts/` | 创建文章 (管理员) |
| PUT | `/api/posts/{post_id}` | 更新文章 (管理员) |
| DELETE | `/api/posts/{post_id}` | 删除文章 (管理员) |

### 分类

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/categories/` | 获取分类列表 |
| POST | `/api/categories/` | 创建分类 (管理员) |
| PUT | `/api/categories/{category_id}` | 更新分类 (管理员) |
| DELETE | `/api/categories/{category_id}` | 删除分类 (管理员) |

### 标签

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/tags/` | 获取标签列表 |
| POST | `/api/tags/` | 创建标签 (管理员) |
| PUT | `/api/tags/{tag_id}` | 更新标签 (管理员) |
| DELETE | `/api/tags/{tag_id}` | 删除标签 (管理员) |

### 评论

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/comments/post/{post_id}` | 获取文章评论 |
| POST | `/api/comments/post/{post_id}` | 添加评论 |
| DELETE | `/api/comments/{comment_id}` | 删除评论 (管理员) |
| GET | `/api/comments/` | 获取所有评论 (管理员) |

### 点赞

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/likes/post/{post_id}` | 点赞/取消点赞文章 |
| GET | `/api/likes/post/{post_id}` | 检查是否已点赞 |

### 管理员

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/admin/stats` | 获取统计数据 |
| POST | `/api/admin/users/{user_id}/promote` | 提升用户为管理员 |

## 项目结构

```
backend/
├── src/
│   ├── routes/           # API 路由
│   │   ├── auth.py       # 认证路由
│   │   ├── posts.py      # 文章路由
│   │   ├── categories.py # 分类路由
│   │   ├── tags.py       # 标签路由
│   │   ├── comments.py   # 评论路由
│   │   ├── likes.py      # 点赞路由
│   │   └── admin.py      # 管理员路由
│   ├── config.py         # 配置管理
│   ├── crud.py           # 数据库操作
│   ├── database.py       # 数据库连接
│   ├── main.py           # 应用入口
│   ├── models.py         # SQLAlchemy 模型
│   ├── schemas.py        # Pydantic 模式
│   └── security.py       # 安全相关
├── scripts/
│   └── init_db.py        # 数据库初始化脚本
├── .env                  # 环境变量
├── pyproject.toml        # 项目配置
└── README.md             # 项目说明
```

## 使用示例

### 注册用户

```bash
curl -X POST "http://localhost:8000/api/auth/register" -H "Content-Type: application/json" -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "password"
}'
```

### 登录获取令牌

```bash
curl -X POST "http://localhost:8000/api/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=user@example.com&password=password"
```

### 获取文章列表

```bash
curl -X GET "http://localhost:8000/api/posts/"
```

### 创建文章 (需要管理员权限)

```bash
curl -X POST "http://localhost:8000/api/posts/" -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_TOKEN" -d '{
    "title": "My First Post",
    "content": "Hello World!",
    "excerpt": "A brief excerpt"
}'
```

### 提升用户为管理员

```bash
curl -X POST "http://localhost:8000/api/admin/users/1/promote" -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

## 许可证

MIT License