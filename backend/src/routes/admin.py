from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas, security
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/stats", response_model=schemas.StatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    return await crud.get_stats(db)

@router.post("/users/{user_id}/promote", response_model=schemas.UserResponse)
async def promote_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    db_user = await crud.promote_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
