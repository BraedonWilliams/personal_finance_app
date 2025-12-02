from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.app.db.database import get_db
from src.app.db.models.category import Category
from src.app.api.schemas.category import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("/", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(
        name=payload.name,
        type=payload.type,          # <-- REQUIRED
        description=payload.description,
        user_id=payload.user_id,
    )

    db.add(category)
    db.commit()
    db.refresh(category)
    return category



@router.get("/", response_model=List[CategoryRead])
def list_categories(user_id: int, db: Session = Depends(get_db)):
    categories = (
        db.query(Category)
        .filter(Category.user_id == user_id)
        .all()
    )
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    update_data = payload.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    db.delete(category)
    db.commit()
    return None
