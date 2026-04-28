from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas, security
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=List[schemas.TagResponse])
async def read_tags(db: AsyncSession = Depends(get_db)):
    return await crud.get_tags(db)

@router.post("/", response_model=schemas.TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag: schemas.TagBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    return await crud.create_tag(db=db, tag=tag)

@router.put("/{tag_id}", response_model=schemas.TagResponse)
async def update_tag(
    tag_id: int,
    tag: schemas.TagBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    db_tag = await crud.update_tag(db=db, tag_id=tag_id, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    success = await crud.delete_tag(db=db, tag_id=tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
