from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from .category import CategoryOut

ISBN13_REGEX = r"^\d{13}$"

class BookCreate(BaseModel):
    title: str = Field(..., max_length=200)
    author: str = Field(..., max_length=100)
    isbn: str = Field(..., min_length=13, max_length=13, pattern=ISBN13_REGEX)
    price: int = Field(..., ge=0)
    stock_quantity: int = Field(0, ge=0)
    published_date: Optional[date] = None
    category_id: Optional[int] = None

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    author: Optional[str] = Field(None, max_length=100)
    price: Optional[int] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    published_date: Optional[date] = None
    category_id: Optional[int] = None

class StockUpdate(BaseModel):
    quantity: int = Field(..., ge=0)
    operation: str = Field(..., pattern=r"^(add|subtract)$")

class BookOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    author: str
    isbn: str
    price: int
    stock_quantity: int
    published_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryOut] = None
