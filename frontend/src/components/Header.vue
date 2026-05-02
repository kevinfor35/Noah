<template>
  <header class="bg-white shadow-sm sticky top-0 z-50">
    <div class="container mx-auto px-4 py-4">
      <div class="flex items-center justify-between">
        <router-link to="/" class="text-2xl font-bold text-blue-600 hover:text-blue-700">
          <BookOpen class="inline-block w-8 h-8 mr-2" />
          Blog
        </router-link>
        
        <nav class="flex items-center space-x-6">
          <router-link to="/" class="text-gray-600 hover:text-blue-600 transition">
            <Home class="inline-block w-5 h-5 mr-1" />
            首页
          </router-link>
          
          <div class="relative">
            <button 
              @click="showCategories = !showCategories"
              class="text-gray-600 hover:text-blue-600 transition flex items-center"
            >
              <Folder class="inline-block w-5 h-5 mr-1" />
              分类
              <ChevronDown class="inline-block w-4 h-4 ml-1" />
            </button>
            <div 
              v-if="showCategories"
              class="absolute top-full left-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg py-2 z-50"
            >
              <router-link 
                v-for="category in categories" 
                :key="category.id"
                :to="{ path: '/', query: { category_id: category.id } }"
                class="block px-4 py-2 text-gray-600 hover:bg-blue-50 hover:text-blue-600 w-40"
                @click="showCategories = false"
              >
                {{ category.name }}
              </router-link>
            </div>
          </div>

          <div class="relative">
            <button 
              @click="showTags = !showTags"
              class="text-gray-600 hover:text-blue-600 transition flex items-center"
            >
              <Tag class="inline-block w-5 h-5 mr-1" />
              标签
              <ChevronDown class="inline-block w-4 h-4 ml-1" />
            </button>
            <div 
              v-if="showTags"
              class="absolute top-full left-0 mt-2 bg-white border border-gray-200 rounded-lg shadow-lg py-2 z-50"
            >
              <router-link 
                v-for="tag in tags" 
                :key="tag.id"
                :to="{ path: '/', query: { tag_id: tag.id } }"
                class="block px-4 py-2 text-gray-600 hover:bg-blue-50 hover:text-blue-600 w-40"
                @click="showTags = false"
              >
                {{ tag.name }}
              </router-link>
            </div>
          </div>

          <div class="relative">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input 
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              type="text" 
              placeholder="搜索文章..." 
              class="pl-10 pr-4 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </nav>

        <div class="flex items-center space-x-4">
          <template v-if="isAuthenticated">
            <span class="text-gray-600">欢迎, {{ user?.username }}</span>
            <router-link 
              v-if="isAdmin" 
              to="/admin" 
              class="text-gray-600 hover:text-blue-600 transition"
            >
              <Settings class="inline-block w-5 h-5" />
            </router-link>
            <button 
              @click="handleLogout" 
              class="text-gray-600 hover:text-red-600 transition"
            >
              <LogOut class="inline-block w-5 h-5" />
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="text-gray-600 hover:text-blue-600 transition">
              <LogIn class="inline-block w-5 h-5" />
              登录
            </router-link>
            <router-link to="/register" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition">
              注册
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../stores/auth'
import { categoriesAPI, tagsAPI } from '../api'
import { BookOpen, Home, Folder, Tag, Search, ChevronDown, LogIn, LogOut, Settings } from 'lucide-vue-next'

const router = useRouter()
const { user, isAuthenticated, isAdmin, logout } = useAuth()

const showCategories = ref(false)
const showTags = ref(false)
const searchQuery = ref('')
const categories = ref([])
const tags = ref([])

onMounted(async () => {
  try {
    const [catRes, tagRes] = await Promise.all([
      categoriesAPI.getCategories(),
      tagsAPI.getTags()
    ])
    categories.value = catRes.data
    tags.value = tagRes.data
  } catch (error) {
    console.error('Failed to load categories/tags:', error)
  }
})

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/', query: { search: searchQuery.value.trim() } })
  }
}

const handleLogout = () => {
  logout()
  router.push('/')
}
</script>
