import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  {
    path: '/post/:id',
    name: 'PostDetail',
    component: () => import('../views/PostDetail.vue')
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/posts',
    name: 'AdminPosts',
    component: () => import('../views/AdminPosts.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/posts/create',
    name: 'CreatePost',
    component: () => import('../views/CreatePost.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/posts/:id/edit',
    name: 'EditPost',
    component: () => import('../views/EditPost.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/categories',
    name: 'AdminCategories',
    component: () => import('../views/AdminCategories.vue'),
    meta: { requiresAdmin: true }
  },
  {
    path: '/admin/tags',
    name: 'AdminTags',
    component: () => import('../views/AdminTags.vue'),
    meta: { requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const { isAuthenticated, isAdmin } = useAuth()
  
  if (to.meta.requiresAdmin) {
    if (!isAuthenticated.value) {
      next('/login')
    } else if (!isAdmin.value) {
      next('/')
    } else {
      next()
    }
  } else if (to.path === '/login' && isAuthenticated.value) {
    next('/')
  } else if (to.path === '/register' && isAuthenticated.value) {
    next('/')
  } else {
    next()
  }
})

export default router
