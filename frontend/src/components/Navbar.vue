<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { categoryApi } from '@/api'
import type { Category } from '@/types'

const userStore = useUserStore()
const router = useRouter()
const categories = ref<Category[]>([])
const searchQuery = ref('')

const fetchCategories = async () => {
  try {
    const response = await categoryApi.getCategories()
    categories.value = response.data
  } catch {
    categories.value = []
  }
}

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/', query: { search: searchQuery.value } })
  }
}

const logout = () => {
  userStore.logout()
  router.push('/')
}

onMounted(fetchCategories)
</script>

<template>
  <nav class="navbar">
    <div class="container">
      <div class="navbar-brand">
        <router-link to="/">Blog</router-link>
      </div>
      
      <div class="navbar-search">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search posts..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">Search</button>
      </div>
      
      <div class="navbar-nav">
        <div class="navbar-categories">
          <span class="category-label">Categories:</span>
          <router-link 
            v-for="cat in categories" 
            :key="cat.id"
            :to="{ path: '/', query: { category_id: cat.id } }"
          >
            {{ cat.name }}
          </router-link>
        </div>
        
        <div v-if="userStore.isLoggedIn" class="auth-links">
          <router-link v-if="userStore.isAdmin" to="/admin">Admin</router-link>
          <button @click="logout">Logout</button>
        </div>
        <div v-else class="auth-links">
          <router-link to="/login">Login</router-link>
          <router-link to="/register">Register</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  background: #333;
  color: white;
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.navbar-brand a {
  color: white;
  text-decoration: none;
}

.navbar-search {
  display: flex;
  gap: 10px;
}

.navbar-search input {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
}

.navbar-search button {
  padding: 8px 16px;
  background: #3b82f6;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
}

.navbar-nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.navbar-categories {
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-label {
  font-size: 14px;
  color: #999;
}

.navbar-categories a {
  color: #ccc;
  text-decoration: none;
  font-size: 14px;
}

.navbar-categories a:hover {
  color: white;
}

.auth-links {
  display: flex;
  gap: 10px;
}

.auth-links a {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 4px;
}

.auth-links a:hover {
  background: rgba(255, 255, 255, 0.1);
}

.auth-links button {
  padding: 8px 16px;
  background: #ef4444;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
}

.auth-links button:hover {
  background: #dc2626;
}
</style>
