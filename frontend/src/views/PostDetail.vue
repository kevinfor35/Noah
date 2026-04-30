<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { postApi, commentApi, likeApi } from '@/api'
import { useUserStore } from '@/stores/user'
import type { Post, Comment } from '@/types'
import Navbar from '@/components/Navbar.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const post = ref<Post | null>(null)
const comments = ref<Comment[]>([])
const newComment = ref('')
const isLiked = ref(false)
const likeCount = ref(0)
const loading = ref(true)
const error = ref('')

const fetchPost = async () => {
  loading.value = true
  try {
    const postId = parseInt(route.params.id as string)
    const response = await postApi.getPost(postId)
    post.value = response.data
    likeCount.value = response.data.like_count
    
    if (userStore.isLoggedIn) {
      const likeResponse = await likeApi.checkLike(postId)
      isLiked.value = likeResponse.data.liked
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to fetch post'
  } finally {
    loading.value = false
  }
}

const fetchComments = async () => {
  try {
    const postId = parseInt(route.params.id as string)
    const response = await commentApi.getComments(postId)
    comments.value = response.data
  } catch {
    comments.value = []
  }
}

const handleLike = async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  try {
    const postId = parseInt(route.params.id as string)
    const response = await likeApi.likePost(postId)
    isLiked.value = response.data.liked
    likeCount.value += isLiked.value ? 1 : -1
  } catch (err: any) {
    console.error('Like failed:', err)
  }
}

const handleComment = async () => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  
  if (!newComment.value.trim()) return
  
  try {
    const postId = parseInt(route.params.id as string)
    await commentApi.createComment(postId, newComment.value)
    newComment.value = ''
    await fetchComments()
    
    if (post.value) {
      post.value.comment_count += 1
    }
  } catch (err: any) {
    console.error('Comment failed:', err)
  }
}

onMounted(() => {
  fetchPost()
  fetchComments()
})
</script>

<template>
  <div class="post-detail">
    <Navbar />
    
    <div class="container">
      <div v-if="loading" class="loading"></div>
      
      <div v-else-if="error" class="error-message">
        {{ error }}
      </div>
      
      <article v-else-if="post" class="post-content">
        <header class="post-header">
          <h1>{{ post.title }}</h1>
          <div class="post-meta">
            <span class="author">By {{ post.author.username }}</span>
            <span class="date">{{ new Date(post.created_at).toLocaleDateString() }}</span>
          </div>
        </header>
        
        <div class="post-tags-bar">
          <span v-if="post.category" class="category">{{ post.category.name }}</span>
          <span v-for="tag in post.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
        </div>
        
        <div class="post-body">
          {{ post.content }}
        </div>
        
        <div class="post-actions">
          <button class="like-btn" :class="{ liked: isLiked }" @click="handleLike">
            <span class="like-icon">{{ isLiked ? '❤️' : '🤍' }}</span>
            <span>{{ likeCount }}</span>
          </button>
          <span class="view-count">👁️ {{ post.view_count }}</span>
          <span class="comment-count">💬 {{ post.comment_count }}</span>
        </div>
        
        <section class="comments-section">
          <h3>Comments ({{ comments.length }})</h3>
          
          <div v-if="comments.length === 0" class="no-comments">
            <p>No comments yet. Be the first to comment!</p>
          </div>
          
          <div v-else class="comments-list">
            <div v-for="comment in comments" :key="comment.id" class="comment">
              <div class="comment-header">
                <span class="comment-author">{{ comment.user.username }}</span>
                <span class="comment-date">{{ new Date(comment.created_at).toLocaleDateString() }}</span>
              </div>
              <p class="comment-content">{{ comment.content }}</p>
            </div>
          </div>
          
          <div class="comment-form">
            <textarea
              v-model="newComment"
              placeholder="Write a comment..."
              :disabled="!userStore.isLoggedIn"
            ></textarea>
            <button
              class="btn btn-primary"
              @click="handleComment"
              :disabled="!userStore.isLoggedIn || !newComment.trim()"
            >
              {{ userStore.isLoggedIn ? 'Submit Comment' : 'Please login to comment' }}
            </button>
          </div>
        </section>
      </article>
    </div>
  </div>
</template>

<style scoped>
.post-detail {
  min-height: 100vh;
}

.error-message {
  text-align: center;
  padding: 40px;
  color: #ef4444;
}

.post-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px 0;
}

.post-header h1 {
  font-size: 2rem;
  margin-bottom: 10px;
}

.post-meta {
  display: flex;
  gap: 15px;
  color: #666;
  margin-bottom: 20px;
}

.post-tags-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.category {
  padding: 5px 12px;
  background: #e0f2fe;
  color: #0369a1;
  border-radius: 4px;
  font-size: 14px;
}

.tag {
  padding: 5px 12px;
  background: #f3f4f6;
  color: #374151;
  border-radius: 4px;
  font-size: 14px;
}

.post-body {
  line-height: 1.8;
  color: #444;
  margin-bottom: 20px;
}

.post-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 15px;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 30px;
}

.like-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.2s;
}

.like-btn:hover {
  background: #fef2f2;
  border-color: #fca5a5;
}

.like-btn.liked {
  background: #fef2f2;
  border-color: #fca5a5;
}

.like-icon {
  font-size: 1.2rem;
}

.view-count,
.comment-count {
  color: #666;
}

.comments-section {
  margin-top: 40px;
}

.comments-section h3 {
  margin-bottom: 20px;
}

.no-comments {
  text-align: center;
  padding: 30px;
  background: #f9fafb;
  border-radius: 8px;
}

.comments-list {
  margin-bottom: 20px;
}

.comment {
  padding: 15px;
  background: #f9fafb;
  border-radius: 8px;
  margin-bottom: 10px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.comment-author {
  font-weight: 500;
}

.comment-date {
  font-size: 14px;
  color: #888;
}

.comment-form textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  min-height: 100px;
  margin-bottom: 10px;
}

.comment-form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
