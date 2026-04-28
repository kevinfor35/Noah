<script setup lang="ts">import { ref, onMounted } from 'vue';
import { categoryApi } from '@/api';
import type { Category } from '@/types';
const categories = ref<Category[]>([]);
const newName = ref('');
const newDescription = ref('');
const editingId = ref<number | null>(null);
const editingName = ref('');
const editingDescription = ref('');
const error = ref('');
const loading = ref(true);
const fetchCategories = async () => {
 loading.value = true;
 try {
 const response = await categoryApi.getCategories();
 categories.value = response.data;
 }
 catch (err: any) {
 console.error('Failed to fetch categories:', err);
 }
 finally {
 loading.value = false;
 }
};
const createCategory = async () => {
 error.value = '';
 if (!newName.value.trim()) {
 error.value = 'Name is required';
 return;
 }
 try {
 await categoryApi.createCategory(newName.value, newDescription.value || undefined);
 newName.value = '';
 newDescription.value = '';
 await fetchCategories();
 }
 catch (err: any) {
 error.value = err.response?.data?.detail || 'Failed to create category';
 }
};
const startEdit = (category: Category) => {
 editingId.value = category.id;
 editingName.value = category.name;
 editingDescription.value = category.description || '';
};
const saveEdit = async () => {
 error.value = '';
 if (!editingName.value.trim()) {
 error.value = 'Name is required';
 return;
 }
 try {
 await categoryApi.updateCategory(editingId.value!, editingName.value, editingDescription.value || undefined);
 editingId.value = null;
 editingName.value = '';
 editingDescription.value = '';
 await fetchCategories();
 }
 catch (err: any) {
 error.value = err.response?.data?.detail || 'Failed to update category';
 }
};
const cancelEdit = () => {
 editingId.value = null;
 editingName.value = '';
 editingDescription.value = '';
};
const deleteCategory = async (id: number) => {
 if (!confirm('Are you sure you want to delete this category?'))
 return;
 try {
 await categoryApi.deleteCategory(id);
 categories.value = categories.value.filter(c => c.id !== id);
 }
 catch (err: any) {
 console.error('Failed to delete category:', err);
 }
};
onMounted(fetchCategories);
</script>

<template>
  <div class="categories-admin">
    <h1>Categories</h1>
    
    <div class="create-form">
      <h3>Add New Category</h3>
      <div class="form-group">
        <input
          v-model="newName"
          type="text"
          placeholder="Category name"
        />
      </div>
      <div class="form-group">
        <input
          v-model="newDescription"
          type="text"
          placeholder="Description (optional)"
        />
      </div>
      <div v-if="error" class="error">{{ error }}</div>
      <button class="btn btn-primary" @click="createCategory">
        Create Category
      </button>
    </div>
    
    <div v-if="loading" class="loading"></div>
    
    <div v-else class="categories-list">
      <div v-if="categories.length === 0" class="no-items">
        <p>No categories found.</p>
      </div>
      
      <div v-for="category in categories" :key="category.id" class="category-item">
        <div v-if="editingId === category.id" class="edit-form">
          <input
            v-model="editingName"
            type="text"
          />
          <input
            v-model="editingDescription"
            type="text"
            placeholder="Description"
          />
          <button class="btn btn-success" @click="saveEdit">Save</button>
          <button class="btn btn-secondary" @click="cancelEdit">Cancel</button>
        </div>
        <div v-else class="category-info">
          <h4>{{ category.name }}</h4>
          <p>{{ category.description || 'No description' }}</p>
          <div class="actions">
            <button class="btn btn-secondary" @click="startEdit(category)">Edit</button>
            <button class="btn btn-danger" @click="deleteCategory(category.id)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.categories-admin h1 {
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

.categories-list {
  display: grid;
  gap: 15px;
}

.category-item {
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

.category-info h4 {
  margin-bottom: 5px;
}

.category-info p {
  color: #666;
  margin-bottom: 10px;
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
