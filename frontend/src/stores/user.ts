import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { authApi } from '@/api'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.is_admin ?? false)

  const login = async (email: string, password: string) => {
    const response = await authApi.login(email, password)
    localStorage.setItem('token', response.data.access_token)
    await fetchUser()
  }

  const register = async (email: string, username: string, password: string) => {
    await authApi.register(email, username, password)
  }

  const fetchUser = async () => {
    try {
      const response = await authApi.getMe()
      user.value = response.data
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch {
      user.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  const logout = () => {
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const initUser = () => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      user.value = JSON.parse(storedUser)
    }
  }

  return {
    user,
    isLoggedIn,
    isAdmin,
    login,
    register,
    fetchUser,
    logout,
    initUser
  }
})
