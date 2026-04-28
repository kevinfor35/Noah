from datetime import datetime
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, desc, or_

from .models import User, Category, Tag, Post, PostTag, Comment, Like
from .schemas import UserCreate, CategoryBase, TagBase, PostCreate, PostUpdate, CommentBase

async def create_user(db: AsyncSession, user: UserCreate) -> User:
    hashed_password = user.password
    from .security import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_category(db: AsyncSession, category: CategoryBase) -> Category:
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category

async def get_categories(db: AsyncSession) -> List[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()

async def get_category_by_id(db: AsyncSession, category_id: int) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()

async def update_category(db: AsyncSession, category_id: int, category: CategoryBase) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    db_category = result.scalars().first()
    if db_category:
        db_category.name = category.name
        db_category.description = category.description
        await db.commit()
        await db.refresh(db_category)
    return db_category

async def delete_category(db: AsyncSession, category_id: int) -> bool:
    result = await db.execute(select(Category).where(Category.id == category_id))
    db_category = result.scalars().first()
    if db_category:
        await db.delete(db_category)
        await db.commit()
        return True
    return False

async def create_tag(db: AsyncSession, tag: TagBase) -> Tag:
    db_tag = Tag(name=tag.name)
    db.add(db_tag)
    await db.commit()
    await db.refresh(db_tag)
    return db_tag

async def get_tags(db: AsyncSession) -> List[Tag]:
    result = await db.execute(select(Tag))
    return result.scalars().all()

async def get_tag_by_id(db: AsyncSession, tag_id: int) -> Optional[Tag]:
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    return result.scalars().first()

async def update_tag(db: AsyncSession, tag_id: int, tag: TagBase) -> Optional[Tag]:
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    db_tag = result.scalars().first()
    if db_tag:
        db_tag.name = tag.name
        await db.commit()
        await db.refresh(db_tag)
    return db_tag

async def delete_tag(db: AsyncSession, tag_id: int) -> bool:
    result = await db.execute(select(Tag).where(Tag.id == tag_id))
    db_tag = result.scalars().first()
    if db_tag:
        await db.delete(db_tag)
        await db.commit()
        return True
    return False

async def create_post(db: AsyncSession, post: PostCreate, author_id: int) -> Post:
    db_post = Post(
        title=post.title,
        content=post.content,
        excerpt=post.excerpt,
        author_id=author_id,
        category_id=post.category_id
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    
    for tag_id in post.tag_ids:
        db_post_tag = PostTag(post_id=db_post.id, tag_id=tag_id)
        db.add(db_post_tag)
    await db.commit()
    
    return db_post

async def get_posts(db: AsyncSession, skip: int = 0, limit: int = 10, category_id: Optional[int] = None, tag_id: Optional[int] = None, search: Optional[str] = None) -> List[Post]:
    query = select(Post).filter(Post.is_published == True)
    
    if category_id:
        query = query.filter(Post.category_id == category_id)
    
    if tag_id:
        query = query.join(PostTag).filter(PostTag.tag_id == tag_id)
    
    if search:
        query = query.filter(or_(
            Post.title.ilike(f"%{search}%"),
            Post.content.ilike(f"%{search}%")
        ))
    
    query = query.order_by(desc(Post.created_at)).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

async def get_post_by_id(db: AsyncSession, post_id: int) -> Optional[Post]:
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalars().first()

async def update_post(db: AsyncSession, post_id: int, post: PostUpdate) -> Optional[Post]:
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalars().first()
    if db_post:
        if post.title is not None:
            db_post.title = post.title
        if post.content is not None:
            db_post.content = post.content
        if post.excerpt is not None:
            db_post.excerpt = post.excerpt
        if post.category_id is not None:
            db_post.category_id = post.category_id
        if post.is_published is not None:
            db_post.is_published = post.is_published
        
        await db.execute(PostTag.__table__.delete().where(PostTag.post_id == post_id))
        
        for tag_id in post.tag_ids or []:
            db_post_tag = PostTag(post_id=post_id, tag_id=tag_id)
            db.add(db_post_tag)
        
        await db.commit()
        await db.refresh(db_post)
    return db_post

async def delete_post(db: AsyncSession, post_id: int) -> bool:
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalars().first()
    if db_post:
        await db.delete(db_post)
        await db.commit()
        return True
    return False

async def increment_view_count(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalars().first()
    if db_post:
        db_post.view_count += 1
        await db.commit()

async def create_comment(db: AsyncSession, comment: CommentBase, post_id: int, user_id: int) -> Comment:
    db_comment = Comment(content=comment.content, post_id=post_id, user_id=user_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def get_comments(db: AsyncSession, post_id: int) -> List[Comment]:
    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id, Comment.is_deleted == False)
        .order_by(Comment.created_at)
    )
    return result.scalars().all()

async def get_all_comments(db: AsyncSession) -> List[Comment]:
    result = await db.execute(
        select(Comment).order_by(desc(Comment.created_at))
    )
    return result.scalars().all()

async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    db_comment = result.scalars().first()
    if db_comment:
        db_comment.is_deleted = True
        await db.commit()
        return True
    return False

async def like_post(db: AsyncSession, post_id: int, user_id: int) -> bool:
    result = await db.execute(select(Like).where(Like.post_id == post_id, Like.user_id == user_id))
    existing_like = result.scalars().first()
    
    if existing_like:
        await db.delete(existing_like)
        await db.commit()
        return False
    
    db_like = Like(post_id=post_id, user_id=user_id)
    db.add(db_like)
    await db.commit()
    return True

async def check_like(db: AsyncSession, post_id: int, user_id: int) -> bool:
    result = await db.execute(select(Like).where(Like.post_id == post_id, Like.user_id == user_id))
    return result.scalars().first() is not None

async def get_like_count(db: AsyncSession, post_id: int) -> int:
    result = await db.execute(select(func.count(Like.id)).where(Like.post_id == post_id))
    return result.scalar() or 0

async def get_comment_count(db: AsyncSession, post_id: int) -> int:
    result = await db.execute(select(func.count(Comment.id)).where(Comment.post_id == post_id, Comment.is_deleted == False))
    return result.scalar() or 0

async def get_stats(db: AsyncSession):
    total_posts = await db.execute(select(func.count(Post.id)))
    total_posts = total_posts.scalar() or 0
    
    total_users = await db.execute(select(func.count(User.id)))
    total_users = total_users.scalar() or 0
    
    total_comments = await db.execute(select(func.count(Comment.id)).where(Comment.is_deleted == False))
    total_comments = total_comments.scalar() or 0
    
    total_likes = await db.execute(select(func.count(Like.id)))
    total_likes = total_likes.scalar() or 0
    
    posts_per_category = await db.execute(
        select(Category.name, func.count(Post.id).label("count"))
        .outerjoin(Post)
        .group_by(Category.id)
    )
    posts_per_category = [{"name": row.name, "count": row.count or 0} for row in posts_per_category.all()]
    
    recent_posts = await db.execute(
        select(Post.id, Post.title, Post.created_at)
        .order_by(desc(Post.created_at))
        .limit(5)
    )
    recent_posts = [{"id": row.id, "title": row.title, "created_at": row.created_at} for row in recent_posts.all()]
    
    return {
        "total_posts": total_posts,
        "total_users": total_users,
        "total_comments": total_comments,
        "total_likes": total_likes,
        "posts_per_category": posts_per_category,
        "recent_posts": recent_posts
    }
