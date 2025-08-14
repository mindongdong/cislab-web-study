from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Category
from app.schemas.category import CategoryCreate, CategoryOut
from app.utils.responses import make_response

router = APIRouter(prefix="/categories", tags=["categories"])

@router.post("", response_model=dict)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(name=payload.name, description=payload.description)
    db.add(category)
    try:
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="category name already exists")
    return make_response("success", CategoryOut.model_validate(category), "category created successfully")

@router.get("", response_model=dict)
def list_categories(db: Session = Depends(get_db)):
    categories = db.execute(select(Category)).scalars().all()
    data = [CategoryOut.model_validate(c) for c in categories]
    return make_response("success", data, "category list retrieved successfully")
