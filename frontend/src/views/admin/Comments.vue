<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { commentApi } from '@/api'
import type { Comment } from '@/types'

const comments = ref<Comment[]>([])
const loading = ref(true)

const fetchComments = async () => {
  loading.value = true
  try {
    const response = await commentApi.getAllComments()
    comments.value = response.data
  } catch (err: any) {
    console.error('Failed to fetch comments:', err)
  } finally {
    loading.value = false
  }
}

const deleteComment = async (id: number) => {
  if (!confirm('Are you sure you want to delete this comment?')) return
  
  try {
    await commentApi.deleteComment(id)
    comments.value = comments.value.filter(c => c.id !== id)
  } catch (err: any) {
    console.error('Failed to delete comment:', err)
  }
}

onMounted(fetchComments)
</script>

<template>
  <div class="comments-admin">
    <h1>Comments</h1>
    
    <div v-if="loading" class="loading"></div>
    
    <div v-else class="comments-list">
      <div v-if="comments.length === 0" class="no-items">
        <p>No comments found.</p>
      </div>
      
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <span class="author">{{ comment.user.username }}</span>
          <span class="date">{{ new Date(comment.created_at).toLocaleString() }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
        <button class="btn btn-danger" @click="deleteComment(comment.id)">
          Delete Comment
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.comments-admin h1 {
  margin-bottom: 20px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.comment-item {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.author {
  font-weight: 500;
}

.date {
  font-size: 14px;
  color: #888;
}

.comment-content {
  margin-bottom: 15px;
  color: #444;
}

.no-items {
  text-align: center;
  padding: 40px;
  background: white;
  border-radius: 8px;
}
</style>
