<template>
  <div class="max-w-6xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">文章管理</h1>
        <p class="text-gray-500">管理博客文章</p>
      </div>
      <router-link 
        to="/admin/posts/create" 
        class="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition flex items-center"
      >
        <Plus class="w-5 h-5 mr-2" />
        创建文章
      </router-link>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <div v-else class="bg-white rounded-lg shadow-md overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">标题</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">作者</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">分类</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">状态</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">创建时间</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="post in posts" :key="post.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap">
              <router-link :to="`/post/${post.id}`" class="text-blue-600 hover:underline">
                {{ post.title }}
              </router-link>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">{{ post.author.username }}</td>
            <td class="px-6 py-4 whitespace-nowrap">{{ post.category?.name || '未分类' }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span 
                :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  post.is_published ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                ]"
              >
                {{ post.is_published ? '已发布' : '草稿' }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">{{ formatDate(post.created_at) }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center space-x-2">
                <router-link 
                  :to="`/admin/posts/${post.id}/edit`" 
                  class="text-blue-600 hover:text-blue-800"
                >
                  <Pencil class="w-5 h-5" />
                </router-link>
                <button 
                  @click="handleDelete(post.id)" 
                  class="text-red-600 hover:text-red-800"
                >
                  <Trash2 class="w-5 h-5" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="posts.length === 0" class="text-center py-12">
        <FileText class="w-12 h-12 text-gray-300 mx-auto mb-2" />
        <p class="text-gray-500">暂无文章</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { postsAPI } from '../api'
import { Loader2, Plus, Pencil, Trash2, FileText } from 'lucide-vue-next'

const loading = ref(false)
const posts = ref([])

const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await postsAPI.getPosts({ limit: 100 })
    posts.value = response.data
  } catch (error) {
    console.error('Failed to fetch posts:', error)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (postId) => {
  if (!confirm('确定要删除这篇文章吗？')) return
  
  try {
    await postsAPI.deletePost(postId)
    posts.value = posts.value.filter(post => post.id !== postId)
  } catch (error) {
    console.error('Failed to delete post:', error)
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchPosts()
})
</script>
