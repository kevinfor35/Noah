<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">管理后台</h1>
      <div class="text-sm text-gray-500">欢迎, {{ user?.username }}</div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">总文章数</p>
            <p class="text-3xl font-bold text-blue-600">{{ stats.total_posts }}</p>
          </div>
          <FileText class="w-12 h-12 text-blue-200" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">总用户数</p>
            <p class="text-3xl font-bold text-green-600">{{ stats.total_users }}</p>
          </div>
          <Users class="w-12 h-12 text-green-200" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">总评论数</p>
            <p class="text-3xl font-bold text-purple-600">{{ stats.total_comments }}</p>
          </div>
          <MessageCircle class="w-12 h-12 text-purple-200" />
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-gray-500 text-sm">总点赞数</p>
            <p class="text-3xl font-bold text-red-600">{{ stats.total_likes }}</p>
          </div>
          <Heart class="w-12 h-12 text-red-200" />
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">文章分类统计</h3>
        <div class="space-y-3">
          <div 
            v-for="item in stats.posts_per_category" 
            :key="item.category_name"
            class="flex items-center"
          >
            <span class="w-24 text-gray-600 text-sm truncate">{{ item.category_name || '未分类' }}</span>
            <div class="flex-1 mx-4 bg-gray-200 rounded-full h-2">
              <div 
                class="bg-blue-600 h-2 rounded-full"
                :style="{ width: `${(item.count / stats.total_posts) * 100}%` }"
              ></div>
            </div>
            <span class="text-gray-600 text-sm">{{ item.count }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">最近文章</h3>
        <div class="space-y-3">
          <div 
            v-for="item in stats.recent_posts" 
            :key="item.id"
            class="flex items-center justify-between"
          >
            <router-link 
              :to="`/post/${item.id}`" 
              class="text-gray-800 hover:text-blue-600 truncate flex-1 mr-4"
            >
              {{ item.title }}
            </router-link>
            <router-link 
              :to="`/admin/posts/${item.id}/edit`" 
              class="text-gray-400 hover:text-blue-600"
            >
              <Pencil class="w-4 h-4" />
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
      <router-link 
        to="/admin/posts" 
        class="bg-blue-600 text-white p-6 rounded-lg hover:bg-blue-700 transition text-center"
      >
        <FileText class="w-8 h-8 mx-auto mb-2" />
        <p>文章管理</p>
      </router-link>
      <router-link 
        to="/admin/categories" 
        class="bg-green-600 text-white p-6 rounded-lg hover:bg-green-700 transition text-center"
      >
        <Folder class="w-8 h-8 mx-auto mb-2" />
        <p>分类管理</p>
      </router-link>
      <router-link 
        to="/admin/tags" 
        class="bg-purple-600 text-white p-6 rounded-lg hover:bg-purple-700 transition text-center"
      >
        <Tag class="w-8 h-8 mx-auto mb-2" />
        <p>标签管理</p>
      </router-link>
      <router-link 
        to="/admin/posts/create" 
        class="bg-red-600 text-white p-6 rounded-lg hover:bg-red-700 transition text-center"
      >
        <Plus class="w-8 h-8 mx-auto mb-2" />
        <p>创建文章</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '../stores/auth'
import { adminAPI } from '../api'
import { Loader2, FileText, Users, MessageCircle, Heart, Pencil, Folder, Tag, Plus } from 'lucide-vue-next'

const { user } = useAuth()

const loading = ref(false)
const stats = ref({
  total_posts: 0,
  total_users: 0,
  total_comments: 0,
  total_likes: 0,
  posts_per_category: [],
  recent_posts: []
})

const fetchStats = async () => {
  loading.value = true
  try {
    const response = await adminAPI.getStats()
    stats.value = response.data
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
})
</script>
