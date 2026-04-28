<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminApi } from '@/api'
import type { Stats } from '@/types'

const stats = ref<Stats | null>(null)
const loading = ref(true)

const fetchStats = async () => {
  loading.value = true
  try {
    const response = await adminApi.getStats()
    stats.value = response.data
  } catch (err: any) {
    console.error('Failed to fetch stats:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchStats)
</script>

<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    
    <div v-if="loading" class="loading"></div>
    
    <div v-else-if="stats" class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_posts }}</div>
          <div class="stat-label">Total Posts</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_users }}</div>
          <div class="stat-label">Total Users</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">💬</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_comments }}</div>
          <div class="stat-label">Total Comments</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">❤️</div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.total_likes }}</div>
          <div class="stat-label">Total Likes</div>
        </div>
      </div>
    </div>
    
    <div class="charts-section">
      <div class="chart-card">
        <h3>Posts per Category</h3>
        <div class="bar-chart">
          <div
            v-for="item in stats?.posts_per_category"
            :key="item.name"
            class="bar-item"
          >
            <span class="bar-label">{{ item.name }}</span>
            <div class="bar-container">
              <div
                class="bar"
                :style="{ width: `${(item.count / (stats?.posts_per_category.reduce((acc, curr) => acc + curr.count, 0) || 1)) * 100}%` }"
              ></div>
            </div>
            <span class="bar-value">{{ item.count }}</span>
          </div>
        </div>
      </div>
      
      <div class="chart-card">
        <h3>Recent Posts</h3>
        <ul class="recent-posts">
          <li
            v-for="post in stats?.recent_posts"
            :key="post.id"
          >
            <a :href="`/post/${post.id}`" target="_blank">{{ post.title }}</a>
            <span>{{ new Date(post.created_at).toLocaleDateString() }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard h1 {
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 2rem;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}

.stat-label {
  color: #666;
  font-size: 14px;
}

.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.chart-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
  margin-bottom: 15px;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bar-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.bar-label {
  width: 100px;
  font-size: 14px;
}

.bar-container {
  flex: 1;
  height: 20px;
  background: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.bar {
  height: 100%;
  background: #3b82f6;
  border-radius: 10px;
  transition: width 0.3s;
}

.bar-value {
  width: 40px;
  text-align: right;
  font-size: 14px;
}

.recent-posts {
  list-style: none;
}

.recent-posts li {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.recent-posts li:last-child {
  border-bottom: none;
}

.recent-posts a {
  color: #3b82f6;
  text-decoration: none;
}

.recent-posts span {
  color: #888;
  font-size: 14px;
}
</style>
