<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { tagApi } from '@/api'
import type { Tag } from '@/types'

const tags = ref<Tag[]>([])
const newName = ref('')
const editingId = ref<number | null>(null)
const editingName = ref('')
const error = ref('')
const loading = ref(true)

const fetchTags = async () => {
  loading.value = true
  try {
    const response = await tagApi.getTags()
    tags.value = response.data
  } catch (err: any) {
    console.error('Failed to fetch tags:', err)
  } finally {
    loading.value = false
  }
}

const createTag = async () => {
  error.value = ''
  
  if (!newName.value.trim()) {
    error.value = 'Name is required'
    return
  }
  
  try {
    await tagApi.createTag(newName.value)
    newName.value = ''
    await fetchTags()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to create tag'
  }
}

const startEdit = (tag: Tag) => {
  editingId.value = tag.id
  editingName.value = tag.name
}

const saveEdit = async () => {
  error.value = ''
  
  if (!editingName.value.trim()) {
    error.value = 'Name is required'
    return
  }
  
  try {
    await tagApi.updateTag(editingId.value!, editingName.value)
    editingId.value = null
    editingName.value = ''
    await fetchTags()
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to update tag'
  }
}

const cancelEdit = () => {
  editingId.value = null
  editingName.value = ''
}

const deleteTag = async (id: number) => {
  if (!confirm('Are you sure you want to delete this tag?')) return
  
  try {
    await tagApi.deleteTag(id)
    tags.value = tags.value.filter(t => t.id !== id)
  } catch (err: any) {
    console.error('Failed to delete tag:', err)
  }
}

onMounted(fetchTags)
</script>

<template>
  <div class="tags-admin">
    <h1>Tags</h1>
    
    <div class="create-form">
      <h3>Add New Tag</h3>
      <div class="form-group">
        <input
          v-model="newName"
          type="text"
          placeholder="Tag name"
        />
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <button class="btn btn-primary" @click="createTag">
        Create Tag
      </button>
    </div>
    
    <div v-if="loading" class="loading"></div>
    
    <div v-else class="tags-list">
      <div v-if="tags.length === 0" class="no-items">
        <p>No tags found.</p>
      </div>
      
      <div class="tags-grid">
        <div v-for="tag in tags" :key="tag.id" class="tag-item">
          <div v-if="editingId === tag.id" class="edit-form">
            <input
              v-model="editingName"
              type="text"
            />
            <button class="btn btn-success" @click="saveEdit">Save</button>
            <button class="btn btn-secondary" @click="cancelEdit">Cancel</button>
          </div>
          <div v-else class="tag-info">
            <span>{{ tag.name }}</span>
            <div class="actions">
              <button class="btn btn-secondary" @click="startEdit(tag)">Edit</button>
              <button class="btn btn-danger" @click="deleteTag(tag.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tags-admin h1 {
  margin-bottom: 20px;
}

.create-form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.create-form h3 {
  margin-bottom: 15px;
}

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
}

.tag-item {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.edit-form input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.tag-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tag-info span {
  font-size: 16px;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 10px;
}

.no-items {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
}
</style>
