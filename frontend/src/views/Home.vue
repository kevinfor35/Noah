<script setup lang="ts">import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { postApi, tagApi } from '@/api';
import type { Post, Tag } from '@/types';
import Navbar from '@/components/Navbar.vue';
const route = useRoute();
const router = useRouter();
const posts = ref<Post[]>([]);
const tags = ref<Tag[]>([]);
const loading = ref(true);
const searchQuery = computed(() => route.query.search as string || '');
const selectedCategory = computed(() => route.query.category_id ? parseInt(route.query.category_id as string) : undefined);
const selectedTag = computed(() => route.query.tag_id ? parseInt(route.query.tag_id as string) : undefined);
const fetchPosts = async () => {
 loading.value = true;
 try {
 const params: Record<string, number | string> = {};
 if (selectedCategory.value !== undefined) {
 params.category_id = selectedCategory.value;
 }
 if (selectedTag.value !== undefined) {
 params.tag_id = selectedTag.value;
 }
 if (searchQuery.value) {
 params.search = searchQuery.value;
 }
 const response = await postApi.getPosts(params);
 posts.value = response.data;
 }
 catch (error) {
 console.error('Failed to fetch posts:', error);
 posts.value = [];
 }
 loading.value = false;
};
const fetchTags = async () => {
 try {
 const response = await tagApi.getTags();
 tags.value = response.data;
 }
 catch {
 tags.value = [];
 }
};
const handleTagClick = (tagId: number) => {
 router.push({ path: '/', query: { tag_id: tagId } });
};
const clearFilters = () => {
 router.push('/');
};
onMounted(() => {
 fetchPosts();
 fetchTags();
});
</script>

<template>
  <div class="home">
    <Navbar />
    
    <div class="container main-content">
      <aside class="sidebar">
        <div class="card">
          <h3>Tags</h3>
          <div class="tags">
            <button
              v-for="tag in tags"
              :key="tag.id"
              :class="{ active: selectedTag === tag.id }"
              @click="handleTagClick(tag.id)"
            >
              {{ tag.name }}
            </button>
          </div>
        </div>
        
        <div v-if="selectedCategory || selectedTag || searchQuery" class="card">
          <button class="clear-filters" @click="clearFilters">
            Clear Filters
          </button>
        </div>
      </aside>
      
      <main class="posts-container">
        <div v-if="loading" class="loading"></div>
        
        <div v-else-if="posts.length === 0" class="no-posts">
          <p>No posts found.</p>
        </div>
        
        <div v-else class="posts-grid">
          <article
            v-for="post in posts"
            :key="post.id"
            class="post-card"
            @click="router.push(`/post/${post.id}`)"
          >
            <h2>{{ post.title }}</h2>
            <p class="excerpt">{{ post.excerpt || post.content.substring(0, 150) }}...</p>
            <div class="post-meta">
              <span class="author">By {{ post.author.username }}</span>
              <span class="date">{{ new Date(post.created_at).toLocaleDateString() }}</span>
            </div>
            <div class="post-stats">
              <span>👁️ {{ post.view_count }}</span>
              <span>❤️ {{ post.like_count }}</span>
              <span>💬 {{ post.comment_count }}</span>
            </div>
            <div v-if="post.category" class="category">
              {{ post.category.name }}
            </div>
            <div class="post-tags">
              <span v-for="tag in post.tags" :key="tag.id" class="tag">
                {{ tag.name }}
              </span>
            </div>
          </article>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
}

.main-content {
  display: flex;
  gap: 20px;
  padding: 20px 0;
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tags button {
  padding: 4px 12px;
  background: #f0f0f0;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 12px;
}

.tags button.active {
  background: #3b82f6;
  color: white;
}

.clear-filters {
  width: 100%;
  padding: 10px;
  background: #f0f0f0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.posts-container {
  flex: 1;
}

.no-posts {
  text-align: center;
  padding: 40px;
}

.posts-grid {
  display: grid;
  gap: 20px;
}

.post-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.post-card h2 {
  margin-bottom: 10px;
  color: #333;
}

.excerpt {
  color: #666;
  margin-bottom: 10px;
}

.post-meta {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #888;
  margin-bottom: 10px;
}

.post-stats {
  display: flex;
  gap: 15px;
  font-size: 14px;
  color: #888;
  margin-bottom: 10px;
}

.category {
  display: inline-block;
  padding: 4px 12px;
  background: #e0f2fe;
  color: #0369a1;
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 10px;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 4px 10px;
  background: #f3f4f6;
  color: #374151;
  border-radius: 4px;
  font-size: 12px;
}
</style>
