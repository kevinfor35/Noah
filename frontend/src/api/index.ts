import axios from 'axios'
import type { User, Post, Category, Tag, Comment, Stats, Token } from '@/types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    throw error
  }
)

export const authApi = {
  register: (email: string, username: string, password: string) =>
    api.post<User>('/auth/register', { email, username, password }),
  
  login: (email: string, password: string) =>
    api.post<Token>('/auth/login', new URLSearchParams({ username: email, password })),
  
  getMe: () => api.get<User>('/auth/me')
}

export const postApi = {
  getPosts: (params: { skip?: number; limit?: number; category_id?: number; tag_id?: number; search?: string }) =>
    api.get<Post[]>('/posts', { params }),
  
  getPost: (id: number) => api.get<Post>(`/posts/${id}`),
  
  createPost: (data: { title: string; content: string; excerpt?: string; category_id?: number; tag_ids?: number[] }) =>
    api.post<Post>('/posts', data),
  
  updatePost: (id: number, data: { title?: string; content?: string; excerpt?: string; category_id?: number; tag_ids?: number[]; is_published?: boolean }) =>
    api.put<Post>(`/posts/${id}`, data),
  
  deletePost: (id: number) => api.delete(`/posts/${id}`)
}

export const categoryApi = {
  getCategories: () => api.get<Category[]>('/categories'),
  
  createCategory: (name: string, description?: string) =>
    api.post<Category>('/categories', { name, description }),
  
  updateCategory: (id: number, name: string, description?: string) =>
    api.put<Category>(`/categories/${id}`, { name, description }),
  
  deleteCategory: (id: number) => api.delete(`/categories/${id}`)
}

export const tagApi = {
  getTags: () => api.get<Tag[]>('/tags'),
  
  createTag: (name: string) => api.post<Tag>('/tags', { name }),
  
  updateTag: (id: number, name: string) => api.put<Tag>(`/tags/${id}`, { name }),
  
  deleteTag: (id: number) => api.delete(`/tags/${id}`)
}

export const commentApi = {
  getComments: (postId: number) => api.get<Comment[]>(`/comments/post/${postId}`),
  
  createComment: (postId: number, content: string) =>
    api.post<Comment>(`/comments/post/${postId}`, { content }),
  
  deleteComment: (id: number) => api.delete(`/comments/${id}`),
  
  getAllComments: () => api.get<Comment[]>('/comments')
}

export const likeApi = {
  likePost: (postId: number) => api.post<{ post_id: number; liked: boolean }>(`/likes/post/${postId}`),
  
  checkLike: (postId: number) => api.get<{ post_id: number; liked: boolean }>(`/likes/post/${postId}`)
}

export const adminApi = {
  getStats: () => api.get<Stats>('/admin/stats')
}
