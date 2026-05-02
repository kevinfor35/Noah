<template>
  <footer class="bg-gray-800 text-white py-8 mt-16">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div>
          <h3 class="text-xl font-bold mb-4">
            <BookOpen class="inline-block w-6 h-6 mr-2" />
            Blog
          </h3>
          <p class="text-gray-400">
            一个基于 FastAPI 和 Vue.js 的现代化博客系统。
          </p>
        </div>
        <div>
          <h4 class="font-semibold mb-4">快速链接</h4>
          <ul class="space-y-2">
            <li>
              <router-link to="/" class="text-gray-400 hover:text-white transition">首页</router-link>
            </li>
            <li v-if="isAdmin">
              <router-link to="/admin" class="text-gray-400 hover:text-white transition">管理后台</router-link>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="font-semibold mb-4">联系方式</h4>
          <p class="text-gray-400">邮箱: contact@example.com</p>
        </div>
      </div>
      <div class="border-t border-gray-700 mt-8 pt-8 text-center text-gray-400">
        <p>&copy; 2024 Blog. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useAuth } from '../stores/auth'
import { BookOpen } from 'lucide-vue-next'

const { isAdmin } = useAuth()
</script>
