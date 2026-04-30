from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas, security
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/post/{post_id}", response_model=List[schemas.CommentResponse])
async def get_post_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    comments = await crud.get_comments(db, post_id=post_id)
    return [schemas.CommentResponse.from_orm(comment) for comment in comments]

@router.post("/post/{post_id}", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    post_id: int,
    comment: schemas.CommentBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    return await crud.create_comment(db=db, comment=comment, post_id=post_id, user_id=current_user.id)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    success = await crud.delete_comment(db=db, comment_id=comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")

@router.get("/", response_model=List[schemas.CommentResponse])
async def get_all_comments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    comments = await crud.get_all_comments(db)
    return [schemas.CommentResponse.from_orm(comment) for comment in comments]
