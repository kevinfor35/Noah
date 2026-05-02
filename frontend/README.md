# Blog Frontend

基于 Vue 3 的博客系统前端应用。

## 功能特性

- **用户认证**: 登录、注册功能
- **文章浏览**: 文章列表、搜索、分类/标签筛选
- **文章详情**: 阅读文章、点赞、评论
- **管理后台**: 文章管理、分类管理、标签管理、统计数据

## 技术栈

- Vue 3
- Vue Router 4
- Vite
- TailwindCSS 3
- Axios
- Lucide Vue Next (图标库)

## 快速开始

### 环境要求

- Node.js 18+
- npm 或 yarn

### 安装依赖

```bash
cd frontend
npm install
```

### 开发模式

```bash
npm run dev
```

服务将在 `http://localhost:5173` 启动。

### 生产构建

```bash
npm run build
```

构建产物将输出到 `dist` 目录。

### 预览构建结果

```bash
npm run preview
```

## 项目结构

```
frontend/
├── src/
│   ├── components/        # 公共组件
│   │   ├── Header.vue     # 导航栏
│   │   └── Footer.vue     # 页脚
│   ├── views/             # 页面组件
│   │   ├── Home.vue       # 首页
│   │   ├── Login.vue      # 登录页
│   │   ├── Register.vue   # 注册页
│   │   ├── PostDetail.vue # 文章详情页
│   │   ├── Admin.vue      # 管理后台首页
│   │   ├── AdminPosts.vue # 文章管理
│   │   ├── CreatePost.vue # 创建文章
│   │   ├── EditPost.vue   # 编辑文章
│   │   ├── AdminCategories.vue # 分类管理
│   │   └── AdminTags.vue  # 标签管理
│   ├── api/               # API 封装
│   │   └── index.js       # API 接口定义
│   ├── stores/            # 状态管理
│   │   └── auth.js        # 认证状态
│   ├── router/            # 路由配置
│   │   └── index.js       # 路由定义
│   ├── App.vue            # 根组件
│   ├── main.js            # 入口文件
│   └── style.css          # 全局样式
├── index.html             # HTML 模板
├── vite.config.js         # Vite 配置
├── tailwind.config.js     # TailwindCSS 配置
├── postcss.config.js      # PostCSS 配置
└── package.json           # 项目配置
```

## 页面路由

| 路径 | 页面 | 描述 |
|------|------|------|
| `/` | Home | 文章列表首页 |
| `/login` | Login | 用户登录 |
| `/register` | Register | 用户注册 |
| `/post/:id` | PostDetail | 文章详情 |
| `/admin` | Admin | 管理后台首页 |
| `/admin/posts` | AdminPosts | 文章管理 |
| `/admin/posts/create` | CreatePost | 创建文章 |
| `/admin/posts/:id/edit` | EditPost | 编辑文章 |
| `/admin/categories` | AdminCategories | 分类管理 |
| `/admin/tags` | AdminTags | 标签管理 |

## 配置说明

### 后端 API 地址

前端默认连接 `http://localhost:8000/api`。如需修改，编辑 `src/api/index.js` 文件中的 `API_BASE_URL` 变量。

### 路由守卫

- `/admin/*` 路径需要管理员权限
- `/login` 和 `/register` 在已登录状态下会重定向到首页

## 使用说明

### 登录

1. 点击右上角"登录"按钮
2. 输入邮箱和密码
3. 登录成功后自动跳转到首页

### 浏览文章

- 在首页可以看到所有已发布的文章
- 支持按分类、标签筛选文章
- 支持关键词搜索
- 点击文章标题进入详情页

### 评论和点赞

- 需要登录才能进行评论和点赞
- 在文章详情页可以查看评论并发表评论
- 点击点赞按钮可以点赞/取消点赞

### 管理后台

- 管理员用户可以访问管理后台
- 在管理后台可以查看统计数据
- 可以管理文章、分类和标签

## 许可证

MIT License