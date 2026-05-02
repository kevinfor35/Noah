<template>
  <div class="max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">标签管理</h1>
        <p class="text-gray-500">管理文章标签</p>
      </div>
    </div>

    <div v-if="loading" class="flex justify-center items-center py-12">
      <Loader2 class="w-8 h-8 text-blue-600 animate-spin" />
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">标签列表</h3>
        
        <div v-if="tags.length === 0" class="text-center py-8">
          <Tag class="w-12 h-12 text-gray-300 mx-auto mb-2" />
          <p class="text-gray-500">暂无标签</p>
        </div>

        <div v-else class="space-y-3">
          <div 
            v-for="tag in tags" 
            :key="tag.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
          >
            <span class="font-medium text-gray-800">{{ tag.name }}</span>
            <div class="flex items-center space-x-2">
              <button 
                @click="editTag(tag)" 
                class="text-blue-600 hover:text-blue-800"
              >
                <Pencil class="w-4 h-4" />
              </button>
              <button 
                @click="handleDelete(tag.id)" 
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
          {{ editing ? '编辑标签' : '创建标签' }}
        </h3>
        
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700 mb-2">名称</label>
            <input 
              v-model="form.name"
              type="text" 
              id="name" 
              placeholder="标签名称"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>

          <div class="flex items-center space-x-4">
            <button 
              type="submit"
              :disabled="loading"
              class="flex-1 bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {{ editing ? '更新标签' : '创建标签' }}
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
import { tagsAPI } from '../api'
import { Loader2, Tag, Pencil, Trash2 } from 'lucide-vue-next'

const loading = ref(false)
const tags = ref([])
const editing = ref(false)
const editingId = ref(null)

const form = reactive({
  name: ''
})

const fetchTags = async () => {
  loading.value = true
  try {
    const response = await tagsAPI.getTags()
    tags.value = response.data
  } catch (error) {
    console.error('Failed to fetch tags:', error)
  } finally {
    loading.value = false
  }
}

const editTag = (tag) => {
  editing.value = true
  editingId.value = tag.id
  form.name = tag.name
}

const cancelEdit = () => {
  editing.value = false
  editingId.value = null
  form.name = ''
}

const handleSubmit = async () => {
  loading.value = true
  
  try {
    if (editing.value) {
      await tagsAPI.updateTag(editingId.value, form)
    } else {
      await tagsAPI.createTag(form)
    }
    cancelEdit()
    await fetchTags()
  } catch (error) {
    console.error('Failed to save tag:', error)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (tagId) => {
  if (!confirm('确定要删除这个标签吗？')) return
  
  try {
    await tagsAPI.deleteTag(tagId)
    await fetchTags()
  } catch (error) {
    console.error('Failed to delete tag:', error)
  }
}

onMounted(() => {
  fetchTags()
})
</script>
