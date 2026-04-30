<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const logout = () => {
  userStore.logout()
  router.push('/')
}

const navItems = [
  { name: 'Dashboard', path: '/admin' },
  { name: 'Posts', path: '/admin/posts' },
  { name: 'Categories', path: '/admin/categories' },
  { name: 'Tags', path: '/admin/tags' },
  { name: 'Comments', path: '/admin/comments' }
]
</script>

<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">Admin Panel</div>
      
      <nav class="nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          :class="{ active: route.path === item.path }"
        >
          {{ item.name }}
        </router-link>
      </nav>
      
      <button class="logout-btn" @click="logout">Logout</button>
    </aside>
    
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background: #1f2937;
  color: white;
  padding: 20px;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 30px;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.nav a {
  padding: 12px 16px;
  color: #9ca3af;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.nav a:hover,
.nav a.active {
  background: #374151;
  color: white;
}

.logout-btn {
  margin-top: auto;
  padding: 12px;
  width: 100%;
  background: #ef4444;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  margin-top: 30px;
}

.logout-btn:hover {
  background: #dc2626;
}

.content {
  flex: 1;
  padding: 20px;
  background: #f3f4f6;
}
</style>
