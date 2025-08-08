from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel

# 제네릭 타입 변수 - 다양한 데이터 타입을 담을 수 있게 함
T = TypeVar('T')

class ResponseBase(BaseModel, Generic[T]):
    """
    API 응답 기본 스키마
    - 모든 API 응답이 이 형식을 따르도록 통일
    """
    status: str  # "success" | "error"
    data: Optional[T] = None  # 실제 데이터
    message: str = ""  # 사용자에게 전달할 메시지
    
    class Config:
        # Pydantic v1 스타일 설정
        orm_mode = True  # SQLAlchemy 모델과의 호환성
        
class PaginationMeta(BaseModel):
    """페이지네이션 메타 정보"""
    page: int
    size: int
    total: int
    total_pages: int
    
class PaginatedResponse(ResponseBase[T]):
    """페이지네이션이 포함된 응답"""
    meta: Optional[PaginationMeta] = None