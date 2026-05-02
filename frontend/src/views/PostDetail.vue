<template>
  <div class="max-w-3xl mx-auto">
    <div v-if="loading" class="flex justify-center items-center py-12">
      <Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <div v-else-if="post" class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="p-8">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm text-gray-500">{{ formatDate(post.created_at) }}</span>
          <span 
            v-if="post.category"
            class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm"
          >
            {{ post.category.name }}
          </span>
        </div>

        <h1 class="text-3xl font-bold text-gray-800 mb-4">{{ post.title }}</h1>

        <div class="flex items-center space-x-4 mb-6">
          <span class="flex items-center text-gray-600">
            <User class="w-5 h-5 mr-2" />
            {{ post.author.username }}
          </span>
          <span class="flex items-center text-gray-500">
            <Eye class="w-4 h-4 mr-1" />
            {{ post.view_count }}
          </span>
          <span class="flex items-center text-gray-500">
            <Heart class="w-4 h-4 mr-1" />
            {{ likeCount }}
          </span>
          <span class="flex items-center text-gray-500">
            <MessageCircle class="w-4 h-4 mr-1" />
            {{ comments.length }}
          </span>
        </div>

        <div class="flex flex-wrap gap-2 mb-6">
          <span 
            v-for="tag in post.tags" 
            :key="tag.id"
            class="bg-gray-100 text-gray-600 px-3 py-1 rounded-full text-sm"
          >
            {{ tag.name }}
          </span>
        </div>

        <div class="prose prose-lg text-gray-700 mb-8" v-html="formatContent(post.content)"></div>

        <div class="flex items-center space-x-4 pt-6 border-t border-gray-200">
          <button 
            @click="handleLike"
            :disabled="!isAuthenticated"
            class="flex items-center space-x-2 px-4 py-2 rounded-lg transition"
            :class="liked ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'"
          >
            <Heart :class="['w-5 h-5', liked ? 'fill-current' : '']" />
            <span>{{ likeCount }}</span>
          </button>
          
          <button 
            @click="showComments = !showComments"
            class="flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition"
          >
            <MessageCircle class="w-5 h-5" />
            <span>{{ comments.length }}</span>
          </button>
        </div>

        <div v-if="!isAuthenticated" class="mt-4 p-4 bg-yellow-100 text-yellow-700 rounded-lg">
          <AlertCircle class="w-5 h-5 inline mr-2" />
          请先登录以点赞或评论
        </div>

        <div v-if="showComments" class="mt-8">
          <h3 class="text-xl font-bold text-gray-800 mb-4">评论 ({{ comments.length }})</h3>

          <div v-if="comments.length === 0" class="text-center py-8">
            <MessageCircle class="w-12 h-12 text-gray-300 mx-auto mb-2" />
            <p class="text-gray-500">暂无评论，快来发表第一条评论吧！</p>
          </div>

          <div v-else class="space-y-4">
            <div 
              v-for="comment in comments" 
              :key="comment.id"
              class="p-4 bg-gray-50 rounded-lg"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="font-semibold text-gray-800">{{ comment.user.username }}</span>
                <span class="text-sm text-gray-500">{{ formatDate(comment.created_at) }}</span>
              </div>
              <p class="text-gray-600">{{ comment.content }}</p>
            </div>
          </div>

          <form v-if="isAuthenticated" @submit.prevent="handleComment" class="mt-6">
            <textarea 
              v-model="commentContent"
              placeholder="写下你的评论..."
              rows="4"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
            <button 
              type="submit"
              :disabled="!commentContent.trim()"
              class="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              发表评论
            </button>
          </form>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <FileText class="w-16 h-16 text-gray-300 mx-auto mb-4" />
      <p class="text-gray-500">文章不存在</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { postsAPI, commentsAPI, likesAPI } from '../api'
import { useAuth } from '../stores/auth'
import { Loader2, User, Eye, Heart, MessageCircle, AlertCircle, FileText } from 'lucide-vue-next'

const route = useRoute()
const { isAuthenticated } = useAuth()

const loading = ref(false)
const post = ref(null)
const comments = ref([])
const liked = ref(false)
const likeCount = ref(0)
const showComments = ref(true)
const commentContent = ref('')

const fetchPost = async () => {
  loading.value = true
  try {
    const response = await postsAPI.getPost(route.params.id)
    post.value = response.data
    likeCount.value = response.data.like_count
    await fetchComments()
    if (isAuthenticated.value) {
      await checkLike()
    }
  } catch (error) {
    console.error('Failed to fetch post:', error)
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    const response = await commentsAPI.getComments(route.params.id)
    comments.value = response.data
  } catch (error) {
    console.error('Failed to fetch comments:', error)
  }
}

const checkLike = async () => {
  try {
    const response = await likesAPI.checkLike(route.params.id)
    liked.value = response.data.liked
  } catch (error) {
    console.error('Failed to check like:', error)
  }
}

const handleLike = async () => {
  if (!isAuthenticated.value) return
  
  try {
    const response = await likesAPI.likePost(route.params.id)
    liked.value = response.data.liked
    likeCount.value += liked.value ? 1 : -1
  } catch (error) {
    console.error('Failed to like:', error)
  }
}

const handleComment = async () => {
  if (!commentContent.value.trim()) return
  
  try {
    await commentsAPI.createComment(route.params.id, { content: commentContent.value })
    commentContent.value = ''
    await fetchComments()
  } catch (error) {
    console.error('Failed to create comment:', error)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatContent = (content) => {
  return content.replace(/\n/g, '<br>')
}

onMounted(() => {
  fetchPost()
})
</script>
