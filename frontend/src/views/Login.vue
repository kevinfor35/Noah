<template>
  <div class="max-w-md mx-auto">
    <div class="bg-white rounded-lg shadow-lg p-8">
      <div class="text-center mb-8">
        <Lock class="w-16 h-16 text-blue-600 mx-auto mb-4" />
        <h1 class="text-2xl font-bold text-gray-800">登录</h1>
        <p class="text-gray-500">欢迎回来，请登录您的账号</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
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
          登录
        </button>
      </form>

      <div class="mt-6 text-center">
        <p class="text-gray-500">
          还没有账号？
          <router-link to="/register" class="text-blue-600 hover:underline">立即注册</router-link>
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
import axios from 'axios'
import { authAPI } from '../api'
import { useAuth } from '../stores/auth'
import { Lock, Mail, Key, Loader2 } from 'lucide-vue-next'

const router = useRouter()
const { login } = useAuth()

const form = reactive({
  email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await authAPI.login(form.email, form.password)
    const token = response.data.access_token
    
    localStorage.setItem('token', token)
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    
    const userResponse = await authAPI.getMe()
    
    login(token, userResponse.data)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.detail || '登录失败，请检查邮箱和密码'
  } finally {
    loading.value = false
  }
}
</script>
