from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas, security
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[schemas.CategoryResponse])
async def read_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)

@router.post("/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: schemas.CategoryBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    return await crud.create_category(db=db, category=category)

@router.put("/{category_id}", response_model=schemas.CategoryResponse)
async def update_category(
    category_id: int,
    category: schemas.CategoryBase,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    db_category = await crud.update_category(db=db, category_id=category_id, category=category)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(security.get_current_admin_user)
):
    success = await crud.delete_category(db=db, category_id=category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
