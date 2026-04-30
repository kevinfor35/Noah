import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/Register.vue')
    },
    {
      path: '/post/:id',
      name: 'PostDetail',
      component: () => import('@/views/PostDetail.vue')
    },
    {
      path: '/admin',
      name: 'Admin',
      component: () => import('@/views/admin/Admin.vue'),
      meta: { requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'AdminDashboard',
          component: () => import('@/views/admin/Dashboard.vue')
        },
        {
          path: 'posts',
          name: 'AdminPosts',
          component: () => import('@/views/admin/Posts.vue')
        },
        {
          path: 'posts/create',
          name: 'AdminCreatePost',
          component: () => import('@/views/admin/CreatePost.vue')
        },
        {
          path: 'posts/:id/edit',
          name: 'AdminEditPost',
          component: () => import('@/views/admin/EditPost.vue')
        },
        {
          path: 'categories',
          name: 'AdminCategories',
          component: () => import('@/views/admin/Categories.vue')
        },
        {
          path: 'tags',
          name: 'AdminTags',
          component: () => import('@/views/admin/Tags.vue')
        },
        {
          path: 'comments',
          name: 'AdminComments',
          component: () => import('@/views/admin/Comments.vue')
        }
      ]
    }
  ]
})

router.beforeEach(async (to) => {
  const userStore = useUserStore()
  
  if (!userStore.isLoggedIn && !['/login', '/register'].includes(to.path)) {
    return '/login'
  }
  
  if (to.meta.requiresAdmin && !userStore.isAdmin) {
    return '/'
  }
})

export default router
