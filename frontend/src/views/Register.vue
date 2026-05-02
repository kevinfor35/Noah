<template>
  <div class="max-w-md mx-auto">
    <div class="bg-white rounded-lg shadow-lg p-8">
      <div class="text-center mb-8">
        <UserPlus class="w-16 h-16 text-blue-600 mx-auto mb-4" />
        <h1 class="text-2xl font-bold text-gray-800">注册</h1>
        <p class="text-gray-500">创建一个新账号</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-2">邮箱</label>
          <div class="relative">
            <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input 
              v-model="form.email"
              type="email" 
              id="email" 
              placeholder="请输入邮箱"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
        </div>

        <div>
          <label for="username" class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
          <div class="relative">
            <User class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input 
              v-model="form.username"
              type="text" 
              id="username" 
              placeholder="请输入用户名"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-gray-700 mb-2">密码</label>
          <div class="relative">
            <Key class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input 
              v-model="form.password"
              type="password" 
              id="password" 
              placeholder="请输入密码"
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              required
            />
          </div>
        </div>

        <button 
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition disabled:opacity-50 flex items-center justify-center"
        >
          <Loader2 v-if="loading" class="w-5 h-5 mr-2 animate-spin" />
          注册
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-500">
          已有账号？
          <router-link to="/login" class="text-blue-600 hover:underline">立即登录</router-link>
        </p>
      </div>

      <div v-if="error" class="mt-4 p-4 bg-red-100 text-red-700 rounded-lg">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api'
import { useAuth } from '../stores/auth'
import { UserPlus, Mail, User, Key, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const { login } = useAuth()

const form = reactive({
  email: '',
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  
  try {
    await authAPI.register(form)
    const loginResponse = await authAPI.login(form.email, form.password)
    const userResponse = await authAPI.getMe()
    
    login(loginResponse.data.access_token, userResponse.data)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>
