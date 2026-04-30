<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi, categoryApi, tagApi } from '@/api'
import type { Post, Category, Tag } from '@/types'

const route = useRoute()
const router = useRouter()

const post = ref<Post | null>(null)
const title = ref('')
const content = ref('')
const excerpt = ref('')
const categoryId = ref<number | null>(null)
const selectedTags = ref<number[]>([])
const isPublished = ref(true)
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])
const error = ref('')
const loading = ref(true)

const fetchPost = async () => {
  loading.value = true
  try {
    const postId = parseInt(route.params.id as string)
    const response = await postApi.getPost(postId)
    post.value = response.data
    title.value = response.data.title
    content.value = response.data.content
    excerpt.value = response.data.excerpt || ''
    categoryId.value = response.data.category?.id || null
    selectedTags.value = response.data.tags.map(t => t.id)
    isPublished.value = response.data.is_published
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to fetch post'
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await categoryApi.getCategories()
    categories.value = response.data
  } catch {
    categories.value = []
  }
}

const fetchTags = async () => {
  try {
    const response = await tagApi.getTags()
    tags.value = response.data
  } catch {
    tags.value = []
  }
}

const toggleTag = (tagId: number) => {
  const index = selectedTags.value.indexOf(tagId)
  if (index > -1) {
    selectedTags.value.splice(index, 1)
  } else {
    selectedTags.value.push(tagId)
  }
}

const handleSubmit = async () => {
  error.value = ''
  
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'Title and content are required'
    return
  }
  
  loading.value = true
  
  try {
    const postId = parseInt(route.params.id as string)
    await postApi.updatePost(postId, {
      title: title.value,
      content: content.value,
      excerpt: excerpt.value || undefined,
      category_id: categoryId.value || undefined,
      tag_ids: selectedTags.value,
      is_published: isPublished.value
    })
    
    router.push('/admin/posts')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to update post'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchPost()
  fetchCategories()
  fetchTags()
})
</script>

<template>
  <div class="edit-post">
    <h1>Edit Post</h1>
    
    <div v-if="loading" class="loading"></div>
    
    <form v-else @submit.prevent="handleSubmit" class="post-form">
      <div class="form-group">
        <label>Title</label>
        <input
          v-model="title"
          type="text"
          placeholder="Enter post title"
          required
        />
      </div>
      
      <div class="form-group">
        <label>Excerpt (optional)</label>
        <textarea
          v-model="excerpt"
          placeholder="Brief summary of the post"
        ></textarea>
      </div>
      
      <div class="form-group">
        <label>Content</label>
        <textarea
          v-model="content"
          placeholder="Write your post content here..."
          required
          rows="10"
        ></textarea>
      </div>
      
      <div class="form-group">
        <label>Category</label>
        <select v-model="categoryId">
          <option :value="null">Select category</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.name }}
          </option>
        </select>
      </div>
      
      <div class="form-group">
        <label>Tags</label>
        <div class="tags-select">
          <button
            v-for="tag in tags"
            :key="tag.id"
            type="button"
            :class="{ active: selectedTags.includes(tag.id) }"
            @click="toggleTag(tag.id)"
          >
            {{ tag.name }}
          </button>
        </div>
      </div>
      
      <div class="form-group">
        <label>
          <input v-model="isPublished" type="checkbox" />
          Published
        </label>
      </div>
      
      <div v-if="error" class="error">{{ error }}</div>
      
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="router.push('/admin/posts')">
          Cancel
        </button>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Updating...' : 'Update Post' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.edit-post h1 {
  margin-bottom: 20px;
}

.post-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tags-select {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.tags-select button {
  padding: 8px 16px;
  background: #f3f4f6;
  border: 1px solid #ddd;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.tags-select button:hover {
  background: #e5e7eb;
}

.tags-select button.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
</style>
