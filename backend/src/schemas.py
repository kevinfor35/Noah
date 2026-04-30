from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_admin: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

class TagResponse(TagBase):
    id: int
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    is_published: Optional[bool] = None

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    excerpt: Optional[str]
    author: UserResponse
    category: Optional[CategoryResponse]
    tags: List[TagResponse]
    view_count: int
    like_count: int
    comment_count: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class PostListResponse(BaseModel):
    id: int
    title: str
    excerpt: Optional[str]
    author: UserResponse
    category: Optional[CategoryResponse]
    tags: List[TagResponse]
    view_count: int
    like_count: int
    comment_count: int
    is_published: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class CommentResponse(CommentBase):
    id: int
    user: UserResponse
    created_at: datetime
    
    class Config:
        from_attributes = True

class LikeResponse(BaseModel):
    post_id: int
    liked: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class StatsResponse(BaseModel):
    total_posts: int
    total_users: int
    total_comments: int
    total_likes: int
    posts_per_category: List[dict]
    recent_posts: List[dict]
