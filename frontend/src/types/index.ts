export interface User {
  id: number
  email: string
  username: string
  is_admin: boolean
  created_at: string
}

export interface Category {
  id: number
  name: string
  description: string | null
}

export interface Tag {
  id: number
  name: string
}

export interface Post {
  id: number
  title: string
  content: string
  excerpt: string | null
  author: User
  category: Category | null
  tags: Tag[]
  view_count: number
  like_count: number
  comment_count: number
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface Comment {
  id: number
  content: string
  user: User
  created_at: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface Stats {
  total_posts: number
  total_users: number
  total_comments: number
  total_likes: number
  posts_per_category: { name: string; count: number }[]
  recent_posts: { id: number; title: string; created_at: string }[]
}
