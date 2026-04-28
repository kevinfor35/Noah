from fastapi import APIRouter, Depends
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
