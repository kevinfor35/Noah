<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { postApi } from '@/api'
import type { Post } from '@/types'

const router = useRouter()
const posts = ref<Post[]>([])
const loading = ref(true)

const fetchPosts = async () => {
  loading.value = true
  try {
    const response = await postApi.getPosts({ limit: 100 })
    posts.value = response.data
  } catch (err: any) {
    console.error('Failed to fetch posts:', err)
  } finally {
    loading.value = false
  }
}

const deletePost = async (id: number) => {
  if (!confirm('Are you sure you want to delete this post?')) return
  
  try {
    await postApi.deletePost(id)
    posts.value = posts.value.filter(p => p.id !== id)
  } catch (err: any) {
    console.error('Failed to delete post:', err)
  }
}

const editPost = (id: number) => {
  router.push(`/admin/posts/${id}/edit`)
}

onMounted(fetchPosts)
</script>

<template>
  <div class="posts-admin">
    <div class="header">
      <h1>Posts</h1>
      <button class="btn btn-primary" @click="router.push('/admin/posts/create')">
        Create New Post
      </button>
    </div>
    
    <div v-if="loading" class="loading"></div>
    
    <div v-else class="posts-table">
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Category</th>
            <th>Views</th>
            <th>Likes</th>
            <th>Comments</th>
            <th>Status</th>
            <th>Created</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in posts" :key="post.id">
            <td>{{ post.title }}</td>
            <td>{{ post.author.username }}</td>
            <td>{{ post.category?.name || '-' }}</td>
            <td>{{ post.view_count }}</td>
            <td>{{ post.like_count }}</td>
            <td>{{ post.comment_count }}</td>
            <td>
              <span :class="['status', { published: post.is_published, draft: !post.is_published }]">
                {{ post.is_published ? 'Published' : 'Draft' }}
              </span>
            </td>
            <td>{{ new Date(post.created_at).toLocaleDateString() }}</td>
            <td>
              <button class="btn btn-secondary" @click="editPost(post.id)">Edit</button>
              <button class="btn btn-danger" @click="deletePost(post.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="posts.length === 0" class="no-posts">
        <p>No posts found.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.posts-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f9fafb;
  font-weight: 600;
}

.status {
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
}

.status.published {
  background: #dcfce7;
  color: #16a34a;
}

.status.draft {
  background: #fef3c7;
  color: #d97706;
}

.no-posts {
  text-align: center;
  padding: 40px;
}
</style>
