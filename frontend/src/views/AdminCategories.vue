<template>
  <div class="max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">分类管理</h1>
        <p class="text-gray-500">管理文章分类</p>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">分类列表</h3>
        
        <div v-if="categories.length === 0" class="text-center py-8">
          <Folder class="w-12 h-12 text-gray-300 mx-auto mb-2" />
          <p class="text-gray-500">暂无分类</p>
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="category in categories" 
            :key="category.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <div>
              <h4 class="font-medium text-gray-800">{{ category.name }}</h4>
              <p class="text-sm text-gray-500">{{ category.description || '无描述' }}</p>
            </div>
            <div class="flex items-center space-x-2">
              <button 
                @click="editCategory(category)" 
                class="text-blue-600 hover:text-blue-800"
              >
                <Pencil class="w-4 h-4" />
              </button>
              <button 
                @click="handleDelete(category.id)" 
                class="text-red-600 hover:text-red-800"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">
          {{ editing ? '编辑分类' : '创建分类' }}
        </h3>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">名称</label>
            <input 
              v-model="form.name"
              type="text" 
              id="name" 
              placeholder="分类名称"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div>
            <label for="description" class="block text-sm font-medium text-gray-700 mb-2">描述</label>
            <textarea 
              v-model="form.description"
              id="description" 
              placeholder="分类描述（可选）"
              rows="3"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            ></textarea>
          </div>

          <div class="flex items-center space-x-4">
            <button 
              type="submit"
              :disabled="loading"
              class="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {{ editing ? '更新分类' : '创建分类' }}
            </button>
            <button 
              v-if="editing"
              type="button"
              @click="cancelEdit"
              class="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition"
            >
              取消
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { categoriesAPI } from '../api'
import { Loader2, Folder, Pencil, Trash2 } from 'lucide-vue-next'

const loading = ref(false)
const categories = ref([])
const editing = ref(false)
const editingId = ref(null)

const form = reactive({
  name: '',
  description: ''
})

const fetchCategories = async () => {
  loading.value = true
  try {
    const response = await categoriesAPI.getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  } finally {
    loading.value = false
  }
}

const editCategory = (category) => {
  editing.value = true
  editingId.value = category.id
  form.name = category.name
  form.description = category.description || ''
}

const cancelEdit = () => {
  editing.value = false
  editingId.value = null
  form.name = ''
  form.description = ''
}

const handleSubmit = async () => {
  loading.value = true
  
  try {
    if (editing.value) {
      await categoriesAPI.updateCategory(editingId.value, form)
    } else {
      await categoriesAPI.createCategory(form)
    }
    cancelEdit()
    await fetchCategories()
  } catch (error) {
    console.error('Failed to save category:', error)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (categoryId) => {
  if (!confirm('确定要删除这个分类吗？')) return
  
  try {
    await categoriesAPI.deleteCategory(categoryId)
    await fetchCategories()
  } catch (error) {
    console.error('Failed to delete category:', error)
  }
}

onMounted(() => {
  fetchCategories()
})
</script>
