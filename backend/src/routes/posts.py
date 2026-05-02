from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .. import crud, schemas, security
from ..database import get_db
from ..models import User, Category, PostTag, Tag

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[schemas.PostListResponse])
async def read_posts(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    tag_id: Optional[int] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(security.get_current_user_optional)
):
    # 如果是管理员，返回所有帖子；否则只返回已发布的
    posts = await crud.get_posts(
        db, skip=skip, limit=limit, category_id=category_id, tag_id=tag_id, search=search,
        include_unpublished=current_user and current_user.is_admin
    )
    result = []

    for post in posts:
        like_count = await crud.get_like_count(db, post.id)
        comment_count = await crud.get_comment_count(db, post.id)

        author_result = await db.execute(select(User).where(User.id == post.author_id))
        author = author_result.scalars().first()

        category = None
        if post.category_id:
            cat_result = await db.execute(select(Category).where(Category.id == post.category_id))
            category = cat_result.scalars().first()

        tag_result = await db.execute(select(PostTag).where(PostTag.post_id == post.id))
        post_tags = tag_result.scalars().all()

        tags = []
        for pt in post_tags:
            tag_item = await crud.get_tag_by_id(db, pt.tag_id)
            if tag_item:
                tags.append(schemas.TagResponse(id=tag_item.id, name=tag_item.name))

        result.append(schemas.PostListResponse(
            id=post.id,
            title=post.title,
            excerpt=post.excerpt,
            author=schemas.UserResponse(
                id=author.id,
                email=author.email,
                username=author.username,
                is_admin=author.is_admin,
                created_at=author.created_at
            ) if author else schemas.UserResponse(
                id=0, email="", username="Unknown", is_admin=False, created_at=post.created_at
            ),
            category=schemas.CategoryResponse(id=category.id, name=category.name, description=category.description) if category else None,
            tags=tags,
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

    author_result = await db.execute(select(User).where(User.id == post.author_id))
    author = author_result.scalars().first()

    category = None
    if post.category_id:
        cat_result = await db.execute(select(Category).where(Category.id == post.category_id))
        category = cat_result.scalars().first()

    tag_result = await db.execute(select(PostTag).where(PostTag.post_id == post_id))
    post_tags = tag_result.scalars().all()

    tags = []
    for pt in post_tags:
        tag_item = await crud.get_tag_by_id(db, pt.tag_id)
        if tag_item:
            tags.append(schemas.TagResponse(id=tag_item.id, name=tag_item.name))

    return schemas.PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        excerpt=post.excerpt,
        author=schemas.UserResponse(
            id=author.id,
            email=author.email,
            username=author.username,
            is_admin=author.is_admin,
            created_at=author.created_at
        ) if author else schemas.UserResponse(
            id=0, email="", username="Unknown", is_admin=False, created_at=post.created_at
        ),
        category=schemas.CategoryResponse(id=category.id, name=category.name, description=category.description) if category else None,
        tags=tags,
        view_count=post.view_count,
        like_count=like_count,
        comment_count=comment_count,
        is_published=post.is_published,
        created_at=post.created_at,
        updated_at=post.updated_at
    )

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: schemas.PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    db_post = await crud.create_post(db=db, post=post_data, author_id=current_user.id)
    like_count = await crud.get_like_count(db, db_post.id)
    comment_count = await crud.get_comment_count(db, db_post.id)

    author_result = await db.execute(select(User).where(User.id == db_post.author_id))
    author = author_result.scalars().first()

    category = None
    if db_post.category_id:
        cat_result = await db.execute(select(Category).where(Category.id == db_post.category_id))
        category = cat_result.scalars().first()

    tag_result = await db.execute(select(PostTag).where(PostTag.post_id == db_post.id))
    post_tags = tag_result.scalars().all()

    tags = []
    for pt in post_tags:
        tag_item = await crud.get_tag_by_id(db, pt.tag_id)
        if tag_item:
            tags.append(schemas.TagResponse(id=tag_item.id, name=tag_item.name))

    return schemas.PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        excerpt=db_post.excerpt,
        author=schemas.UserResponse(
            id=author.id,
            email=author.email,
            username=author.username,
            is_admin=author.is_admin,
            created_at=author.created_at
        ) if author else schemas.UserResponse(
            id=0, email="", username="Unknown", is_admin=False, created_at=db_post.created_at
        ),
        category=schemas.CategoryResponse(id=category.id, name=category.name, description=category.description) if category else None,
        tags=tags,
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
    post_data: schemas.PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    db_post = await crud.update_post(db=db, post_id=post_id, post=post_data)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    like_count = await crud.get_like_count(db, db_post.id)
    comment_count = await crud.get_comment_count(db, db_post.id)

    author_result = await db.execute(select(User).where(User.id == db_post.author_id))
    author = author_result.scalars().first()

    category = None
    if db_post.category_id:
        cat_result = await db.execute(select(Category).where(Category.id == db_post.category_id))
        category = cat_result.scalars().first()

    tag_result = await db.execute(select(PostTag).where(PostTag.post_id == post_id))
    post_tags = tag_result.scalars().all()

    tags = []
    for pt in post_tags:
        tag_item = await crud.get_tag_by_id(db, pt.tag_id)
        if tag_item:
            tags.append(schemas.TagResponse(id=tag_item.id, name=tag_item.name))

    return schemas.PostResponse(
        id=db_post.id,
        title=db_post.title,
        content=db_post.content,
        excerpt=db_post.excerpt,
        author=schemas.UserResponse(
            id=author.id,
            email=author.email,
            username=author.username,
            is_admin=author.is_admin,
            created_at=author.created_at
        ) if author else schemas.UserResponse(
            id=0, email="", username="Unknown", is_admin=False, created_at=db_post.created_at
        ),
        category=schemas.CategoryResponse(id=category.id, name=category.name, description=category.description) if category else None,
        tags=tags,
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
