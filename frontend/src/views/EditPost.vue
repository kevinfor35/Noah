<template>
  <div class="max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">编辑文章</h1>
        <p class="text-gray-500">修改文章内容</p>
      </div>
      <router-link 
        to="/admin/posts" 
        class="text-gray-600 hover:text-gray-800"
      >
        <ArrowLeft class="w-5 h-5" />
        返回
      </router-link>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <form v-else @submit.prevent="handleSubmit" class="bg-white rounded-lg shadow-md p-8">
      <div class="space-y-6">
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 mb-2">标题</label>
          <input 
            v-model="form.title"
            type="text" 
            id="title" 
            placeholder="请输入文章标题"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          />
        </div>

        <div>
          <label for="excerpt" class="block text-sm font-medium text-gray-700 mb-2">摘要</label>
          <textarea 
            v-model="form.excerpt"
            id="excerpt" 
            placeholder="文章摘要（可选）"
            rows="3"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          ></textarea>
        </div>

        <div>
          <label for="content" class="block text-sm font-medium text-gray-700 mb-2">内容</label>
          <textarea 
            v-model="form.content"
            id="content" 
            placeholder="文章内容"
            rows="10"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required
          ></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">分类</label>
          <select 
            v-model="form.category_id"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option :value="null">未分类</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">标签</label>
          <div class="flex flex-wrap gap-2">
            <span 
              v-for="tag in selectedTags" 
              :key="tag.id"
              class="bg-blue-100 text-blue-600 px-3 py-1 rounded-full text-sm flex items-center"
            >
              {{ tag.name }}
              <button @click="removeTag(tag.id)" class="ml-1">
                <X class="w-4 h-4" />
              </button>
            </span>
          </div>
          <div class="mt-2">
            <select 
              v-model="newTagId"
              class="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">选择标签</option>
              <option 
                v-for="tag in availableTags" 
                :key="tag.id" 
                :value="tag.id"
              >
                {{ tag.name }}
              </option>
            </select>
            <button 
              type="button"
              @click="addTag"
              class="ml-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition"
            >
              添加
            </button>
          </div>
        </div>

        <div class="flex items-center">
          <input 
            v-model="form.is_published"
            type="checkbox" 
            id="is_published"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <label for="is_published" class="ml-2 text-sm text-gray-700">发布文章</label>
        </div>

        <div class="flex items-center space-x-4">
          <button 
            type="submit"
            :disabled="loading"
            class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 flex items-center"
          >
            <Loader2 v-if="loading" class="w-5 h-5 mr-2 animate-spin" />
            更新文章
          </button>
          <router-link 
            to="/admin/posts" 
            class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
          >
            取消
          </router-link>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postsAPI, categoriesAPI, tagsAPI } from '../api'
import { ArrowLeft, X, Loader2 } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const categories = ref([])
const tags = ref([])
const newTagId = ref('')

const form = reactive({
  title: '',
  excerpt: '',
  content: '',
  category_id: null,
  tag_ids: [],
  is_published: true
})

const selectedTags = computed(() => {
  return tags.value.filter(tag => form.tag_ids.includes(tag.id))
})

const availableTags = computed(() => {
  return tags.value.filter(tag => !form.tag_ids.includes(tag.id))
})

const fetchPost = async () => {
  try {
    const response = await postsAPI.getPost(route.params.id)
    const post = response.data
    form.title = post.title
    form.excerpt = post.excerpt || ''
    form.content = post.content
    form.category_id = post.category?.id || null
    form.tag_ids = post.tags.map(tag => tag.id)
    form.is_published = post.is_published
  } catch (error) {
    console.error('Failed to fetch post:', error)
  }
}

const fetchCategories = async () => {
  try {
    const response = await categoriesAPI.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

const fetchTags = async () => {
  try {
    const response = await tagsAPI.getTags()
    tags.value = response.data
  } catch (error) {
    console.error('Failed to fetch tags:', error)
  }
}

const addTag = () => {
  if (newTagId.value && !form.tag_ids.includes(parseInt(newTagId.value))) {
    form.tag_ids.push(parseInt(newTagId.value))
    newTagId.value = ''
  }
}

const removeTag = (tagId) => {
  form.tag_ids = form.tag_ids.filter(id => id !== tagId)
}

const handleSubmit = async () => {
  loading.value = true
  
  try {
    await postsAPI.updatePost(route.params.id, form)
    router.push('/admin/posts')
  } catch (error) {
    console.error('Failed to update post:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await Promise.all([fetchPost(), fetchCategories(), fetchTags()])
  loading.value = false
})
</script>
