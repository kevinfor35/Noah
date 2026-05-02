# Noah Blog

一个基于 FastAPI 和 Vue 3 的现代化博客系统。

## 项目结构

```
Noah/
├── backend/          # 后端 API
│   ├── src/          # 源代码
│   ├── scripts/      # 脚本
│   ├── pyproject.toml
│   └── README.md
├── frontend/         # 前端应用
│   ├── src/          # 源代码
│   ├── package.json
│   └── README.md
└── .gitignore
```

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- SQLAlchemy 2.0 (异步)
- PostgreSQL
- JWT 认证

### 前端
- Vue 3
- Vue Router 4
- Vite
- TailwindCSS 3
- Axios

## 快速开始

### 后端

```bash
cd backend
uv install
# 配置 .env 文件
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 功能特性

- 用户注册和登录
- 文章管理（创建、编辑、删除）
- 分类和标签
- 评论系统
- 点赞功能
- 管理员后台
- 数据统计

## 详细文档

- [后端文档](backend/README.md)
- [前端文档](frontend/README.md)

## 许可证

MIT License