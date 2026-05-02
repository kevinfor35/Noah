import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    return axios.post(`${API_BASE_URL}/auth/login`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },
  getMe: () => api.get('/auth/me')
}

export const postsAPI = {
  getPosts: (params) => api.get('/posts', { params }),
  getPost: (id) => api.get(`/posts/${id}`),
  createPost: (data) => api.post('/posts', data),
  updatePost: (id, data) => api.put(`/posts/${id}`, data),
  deletePost: (id) => api.delete(`/posts/${id}`)
}

export const categoriesAPI = {
  getCategories: () => api.get('/categories'),
  createCategory: (data) => api.post('/categories', data),
  updateCategory: (id, data) => api.put(`/categories/${id}`, data),
  deleteCategory: (id) => api.delete(`/categories/${id}`)
}

export const tagsAPI = {
  getTags: () => api.get('/tags'),
  createTag: (data) => api.post('/tags', data),
  updateTag: (id, data) => api.put(`/tags/${id}`, data),
  deleteTag: (id) => api.delete(`/tags/${id}`)
}

export const commentsAPI = {
  getComments: (postId) => api.get(`/comments/post/${postId}`),
  createComment: (postId, data) => api.post(`/comments/post/${postId}`, data),
  deleteComment: (id) => api.delete(`/comments/${id}`)
}

export const likesAPI = {
  likePost: (postId) => api.post(`/likes/post/${postId}`),
  checkLike: (postId) => api.get(`/likes/post/${postId}`)
}

export const adminAPI = {
  getStats: () => api.get('/admin/stats'),
  promoteUser: (userId) => api.post(`/admin/users/${userId}/promote`)
}

export default api
