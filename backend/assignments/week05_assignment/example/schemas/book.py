"""
Book 관련 Pydantic 스키마
- 복잡한 검증 로직과 다양한 요청/응답 형식 처리
"""
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
import re

class BookBase(BaseModel):
    """도서 기본 스키마"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="도서 제목"
    )
    author: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="저자명"
    )
    isbn: str = Field(
        ...,
        regex="^[0-9]{13}$",
        description="13자리 ISBN"
    )
    price: int = Field(
        ...,
        ge=0,
        description="가격 (0 이상)"
    )
    stock_quantity: int = Field(
        default=0,
        ge=0,
        description="재고 수량 (0 이상)"
    )
    published_date: Optional[date] = Field(
        None,
        description="출간일"
    )
    category_id: Optional[int] = Field(
        None,
        description="카테고리 ID"
    )
    
    @validator('title', 'author')
    def strip_strings(cls, v):
        """문자열 앞뒤 공백 제거"""
        return v.strip()
    
    @validator('isbn')
    def validate_isbn(cls, v):
        """ISBN 형식 검증 - 13자리 숫자"""
        if not re.match(r'^[0-9]{13}$', v):
            raise ValueError("ISBN은 13자리 숫자여야 합니다")
        return v
    
    @validator('published_date')
    def validate_published_date(cls, v):
        """출간일이 미래가 아닌지 검증"""
        if v and v > date.today():
            raise ValueError("출간일은 미래일 수 없습니다")
        return v

class BookCreate(BookBase):
    """도서 생성 요청 스키마"""
    pass

class BookUpdate(BaseModel):
    """
    도서 수정 요청 스키마
    - PATCH 메서드를 위해 모든 필드가 선택적
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, regex="^[0-9]{13}$")
    price: Optional[int] = Field(None, ge=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    published_date: Optional[date] = None
    category_id: Optional[int] = None
    
    @validator('title', 'author')
    def strip_strings(cls, v):
        return v.strip() if v else v
    
    @validator('isbn')
    def validate_isbn(cls, v):
        if v and not re.match(r'^[0-9]{13}$', v):
            raise ValueError("ISBN은 13자리 숫자여야 합니다")
        return v
    
    @validator('published_date')
    def validate_published_date(cls, v):
        if v and v > date.today():
            raise ValueError("출간일은 미래일 수 없습니다")
        return v

class BookResponse(BookBase):
    """도서 응답 스키마"""
    id: int
    created_at: datetime
    updated_at: datetime
    category_name: Optional[str] = None  # 카테고리명 포함
    
    class Config:
        orm_mode = True

class StockUpdateRequest(BaseModel):
    """재고 수정 요청 스키마"""
    quantity: int = Field(..., gt=0, description="변경할 수량 (양수)")
    operation: str = Field(..., regex="^(add|subtract)$", description="add 또는 subtract")
    
    @validator('operation')
    def validate_operation(cls, v):
        if v not in ['add', 'subtract']:
            raise ValueError("operation은 'add' 또는 'subtract'만 가능합니다")
        return v

class BookSearchParams(BaseModel):
    """도서 검색 파라미터"""
    search: Optional[str] = Field(None, description="검색어 (제목/저자)")
    category_id: Optional[int] = Field(None, gt=0, description="카테고리 ID")
    min_price: Optional[int] = Field(None, ge=0, description="최소 가격")
    max_price: Optional[int] = Field(None, ge=0, description="최대 가격")
    page: int = Field(1, gt=0, description="페이지 번호")
    size: int = Field(10, gt=0, le=100, description="페이지 크기")
    
    @validator('max_price')
    def validate_price_range(cls, v, values):
        """최대 가격이 최소 가격보다 크거나 같은지 검증"""
        min_price = values.get('min_price')
        if min_price is not None and v is not None and v < min_price:
            raise ValueError("최대 가격은 최소 가격보다 크거나 같아야 합니다")
        return v