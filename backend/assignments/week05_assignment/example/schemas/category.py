"""
Category 관련 Pydantic 스키마
- 요청/응답 데이터 검증 및 직렬화
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator

class CategoryBase(BaseModel):
    """카테고리 기본 스키마"""
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="카테고리명"
    )
    description: Optional[str] = Field(
        None,
        description="카테고리 설명"
    )
    
    @validator('name')
    def validate_name(cls, v):
        """카테고리명 검증"""
        if not v or v.strip() == "":
            raise ValueError("카테고리명은 필수입니다")
        return v.strip()

class CategoryCreate(CategoryBase):
    """카테고리 생성 요청 스키마"""
    pass

class CategoryUpdate(BaseModel):
    """카테고리 수정 요청 스키마 - 모든 필드 선택적"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    
    @validator('name')
    def validate_name(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("카테고리명은 비어있을 수 없습니다")
        return v.strip() if v else v

class CategoryResponse(CategoryBase):
    """카테고리 응답 스키마"""
    id: int
    created_at: datetime
    book_count: Optional[int] = 0  # 해당 카테고리의 도서 수
    
    class Config:
        orm_mode = True
        
class CategoryWithBooks(CategoryResponse):
    """도서 목록이 포함된 카테고리 응답"""
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .book import BookResponse
    
    books: List['BookResponse'] = []