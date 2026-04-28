<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { postApi, categoryApi, tagApi } from '@/api'
import type { Category, Tag } from '@/types'

const router = useRouter()

const title = ref('')
const content = ref('')
const excerpt = ref('')
const categoryId = ref<number | null>(null)
const selectedTags = ref<number[]>([])
const categories = ref<Category[]>([])
const tags = ref<Tag[]>([])
const error = ref('')
const loading = ref(false)

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
    await postApi.createPost({
      title: title.value,
      content: content.value,
      excerpt: excerpt.value || undefined,
      category_id: categoryId.value || undefined,
      tag_ids: selectedTags.value.length > 0 ? selectedTags.value : undefined
    })
    
    router.push('/admin/posts')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to create post'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchTags()
})
</script>

<template>
  <div class="create-post">
    <h1>Create New Post</h1>
    
    <form @submit.prevent="handleSubmit" class="post-form">
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
      
      <div v-if="error" class="error">{{ error }}</div>
      
      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="router.push('/admin/posts')">
          Cancel
        </button>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Creating...' : 'Create Post' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.create-post h1 {
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
