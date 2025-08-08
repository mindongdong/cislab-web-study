from pydantic import BaseModel, Field
from datetime import date
from typing import Literal

# pydentic을 이용한 request body 정의
class CreateBookRequest(BaseModel):
    title: str
    author: str
    isbn: str | None = None
    price: int
    stock_quantity: int | None = 0
    published_date: date | None = None

    category_id: int | None = None

class UpdateBookRequest(BaseModel):
    price: int | None = None
    stock_quantity: int | None = None

class UpdateStockRequest(BaseModel):
    quantity: int = Field(..., gt=0, description="변경할 재고 수량")
    operation: Literal["add", "subtract"] = Field(..., description="재고 추가 또는 차감")

class CreateCategoryRequest(BaseModel):
    name: str
    description: str | None = None



