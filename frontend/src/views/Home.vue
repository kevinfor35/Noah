<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-8">
      <h1 class="text-4xl font-bold text-gray-800 mb-2">最新文章</h1>
      <p class="text-gray-500">阅读最新发布的博客文章</p>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <div v-else-if="posts.length === 0" class="text-center py-12">
      <FileText class="w-16 h-16 text-gray-300 mx-auto mb-4" />
      <p class="text-gray-500">暂无文章</p>
    </div>

    <div v-else class="space-y-6">
      <article 
        v-for="post in posts" 
        :key="post.id"
        class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition"
      >
        <div class="p-6">
          <div class="flex items-center justify-between mb-3">
            <span class="text-sm text-gray-500">{{ formatDate(post.created_at) }}</span>
            <span 
              v-if="post.category"
              class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm"
            >
              {{ post.category.name }}
            </span>
          </div>
          
          <h2 class="text-xl font-bold text-gray-800 mb-2">
            <router-link :to="`/post/${post.id}`" class="hover:text-blue-600 transition">
              {{ post.title }}
            </router-link>
          </h2>
          
          <p class="text-gray-600 mb-4 line-clamp-2">{{ post.excerpt || post.content }}</p>
          
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <span class="flex items-center text-gray-500">
                <User class="w-4 h-4 mr-1" />
                {{ post.author.username }}
              </span>
              <span class="flex items-center text-gray-500">
                <Eye class="w-4 h-4 mr-1" />
                {{ post.view_count }}
              </span>
              <span class="flex items-center text-gray-500">
                <Heart class="w-4 h-4 mr-1" />
                {{ post.like_count }}
              </span>
              <span class="flex items-center text-gray-500">
                <MessageCircle class="w-4 h-4 mr-1" />
                {{ post.comment_count }}
              </span>
            </div>
            
            <div class="flex items-center space-x-2">
              <span 
                v-for="tag in post.tags" 
                :key="tag.id"
                class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-sm"
              >
                {{ tag.name }}
              </span>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div v-if="hasMore" class="flex justify-center mt-8">
      <button 
        @click="loadMore"
        class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition flex items-center"
      >
        <RefreshCw class="w-4 h-4 mr-2" />
        加载更多
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { postsAPI } from '../api'
import { Loader2, FileText, User, Eye, Heart, MessageCircle, RefreshCw } from 'lucide-vue-next'

const route = useRoute()
const posts = ref([])
const loading = ref(false)
const skip = ref(0)
const limit = 10
const hasMore = ref(true)

const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {
      skip: skip.value,
      limit: limit
    }
    
    if (route.query.category_id) {
      params.category_id = parseInt(route.query.category_id)
    }
    if (route.query.tag_id) {
      params.tag_id = parseInt(route.query.tag_id)
    }
    if (route.query.search) {
      params.search = route.query.search
    }
    
    const response = await postsAPI.getPosts(params)
    if (response.data.length < limit) {
      hasMore.value = false
    }
    posts.value = [...posts.value, ...response.data]
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  } finally {
    loading.value = false
  }
}

const loadMore = () => {
  skip.value += limit
  fetchPosts()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchPosts()
})

watch(() => route.query, () => {
  posts.value = []
  skip.value = 0
  hasMore.value = true
  fetchPosts()
}, { deep: true })
</script>
