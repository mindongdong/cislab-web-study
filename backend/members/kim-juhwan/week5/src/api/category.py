from typing import List

from database.connection import get_db
from database.orm import Category
from database.repository import get_categories, create_category
from fastapi import Depends, APIRouter

from schema.request import CreateCategoryRequest
from schema.response import CategoryListSchema, CategorySchema
from sqlalchemy.orm import Session

router = APIRouter(prefix="/categories")

@router.get("", status_code=200)
def get_categories_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
) -> CategoryListSchema:
    categories: List[Category] = get_categories(session=session)

    if order and order == "DESC":
        return CategoryListSchema(
            categories=[CategorySchema.from_orm(category) for category in categories[::-1]]
        )
    return CategoryListSchema(
        categories=[CategorySchema.from_orm(category) for category in categories]
    )


@router.post("", status_code=201)
def create_category_handler(
        request: CreateCategoryRequest,
        session: Session = Depends(get_db),
) -> CategorySchema:
    category: Category = Category.create(request=request) # id=None
    category: Category = create_category(session=session, category=category) # id=int
    return CategorySchema.from_orm(category)
