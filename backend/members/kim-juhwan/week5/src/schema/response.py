from typing import List
from datetime import date, datetime

from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    isbn: str | None = None
    price: int
    stock_quantity: int | None = 0
    published_date: date | None = None
    created_at: datetime                    # 'TIMESTAMP' 타입은 'datetime'으로 매핑
    updated_at: datetime                    # 'TIMESTAMP' 타입은 'datetime'으로 매핑
    category_id: int | None = None

    class Config:
        orm_mode = True


class BookListSchema(BaseModel):
    books: List[BookSchema]


class CategorySchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    created_at: datetime

    class Config:
        orm_mode = True

class CategoryListSchema(BaseModel):
    categories: List[CategorySchema]