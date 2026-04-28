from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas, security
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/likes", tags=["likes"])

@router.post("/post/{post_id}", response_model=schemas.LikeResponse)
async def like_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    liked = await crud.like_post(db=db, post_id=post_id, user_id=current_user.id)
    return {"post_id": post_id, "liked": liked}

@router.get("/post/{post_id}", response_model=schemas.LikeResponse)
async def check_like(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    liked = await crud.check_like(db=db, post_id=post_id, user_id=current_user.id)
    return {"post_id": post_id, "liked": liked}
