from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas, security
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.PostListResponse])
async def read_posts(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    posts = await crud.get_posts(db, skip=skip, limit=limit, category_id=category_id, tag_id=tag_id, search=search)
    result = []
    for post in posts:
        like_count = await crud.get_like_count(db, post.id)
        comment_count = await crud.get_comment_count(db, post.id)
        result.append(schemas.PostListResponse(
            id=post.id,
            title=post.title,
            excerpt=post.excerpt,
            author=schemas.UserResponse.from_orm(post.author),
            category=schemas.CategoryResponse.from_orm(post.category) if post.category else None,
            tags=[schemas.TagResponse.from_orm(pt.tag) for pt in post.tags],
            view_count=post.view_count,
            like_count=like_count,
            comment_count=comment_count,
            is_published=post.is_published,
            created_at=post.created_at
        ))
    return result

@router.get("/{post_id}", response_model=schemas.PostResponse)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post_by_id(db, post_id=post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await crud.increment_view_count(db, post_id)
    
    like_count = await crud.get_like_count(db, post_id)
    comment_count = await crud.get_comment_count(db, post_id)
    
    return schemas.PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        excerpt=post.excerpt,
        author=schemas.UserResponse.from_orm(post.author),
        category=schemas.CategoryResponse.from_orm(post.category) if post.category else None,
        tags=[schemas.TagResponse.from_orm(pt.tag) for pt in post.tags],
        view_count=post.view_count,
        like_count=like_count,
        comment_count=comment_count,
        is_published=post.is_published,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    db_post = await crud.create_post(db=db, post=post, author_id=current_user.id)
    like_count = await crud.get_like_count(db, db_post.id)
    comment_count = await crud.get_comment_count(db, db_post.id)
    
    return schemas.PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        excerpt=db_post.excerpt,
        author=schemas.UserResponse.from_orm(db_post.author),
        category=schemas.CategoryResponse.from_orm(db_post.category) if db_post.category else None,
        tags=[schemas.TagResponse.from_orm(pt.tag) for pt in db_post.tags],
        view_count=db_post.view_count,
        like_count=like_count,
        comment_count=comment_count,
        is_published=db_post.is_published,
        created_at=db_post.created_at,
        updated_at=db_post.updated_at
    )

@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(
    post_id: int,
    post: schemas.PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    db_post = await crud.update_post(db=db, post_id=post_id, post=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    like_count = await crud.get_like_count(db, db_post.id)
    comment_count = await crud.get_comment_count(db, db_post.id)
    
    return schemas.PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        excerpt=db_post.excerpt,
        author=schemas.UserResponse.from_orm(db_post.author),
        category=schemas.CategoryResponse.from_orm(db_post.category) if db_post.category else None,
        tags=[schemas.TagResponse.from_orm(pt.tag) for pt in db_post.tags],
        view_count=db_post.view_count,
        like_count=like_count,
        comment_count=comment_count,
        is_published=db_post.is_published,
        created_at=db_post.created_at,
        updated_at=db_post.updated_at
    )

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    success = await crud.delete_post(db=db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
