"""
Category API 엔드포인트
- RESTful API 설계 원칙 준수
- 일관된 응답 형식 적용
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.category import (
    CategoryCreate, CategoryUpdate, CategoryResponse
)
from app.schemas.common import ResponseBase, PaginatedResponse
from app.services.category_service import CategoryService
from app.utils.exceptions import BusinessException

# 라우터 인스턴스 생성
router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    responses={404: {"description": "Not found"}}
)

@router.post(
    "",
    response_model=ResponseBase[CategoryResponse],
    status_code=status.HTTP_201_CREATED,
    summary="카테고리 생성",
    description="새로운 도서 카테고리를 생성합니다."
)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
) -> ResponseBase[CategoryResponse]:
    """
    카테고리 생성 엔드포인트
    - 중복된 카테고리명 체크
    - 성공 시 201 Created 반환
    """
    try:
        category = CategoryService.create_category(db, category_data)
        return ResponseBase(
            status="success",
            data=CategoryResponse.from_orm(category),
            message="카테고리가 성공적으로 생성되었습니다"
        )
    except BusinessException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"status": "error", "message": e.message}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "서버 오류가 발생했습니다"}
        )

@router.get(
    "",
    response_model=ResponseBase[List[CategoryResponse]],
    summary="전체 카테고리 조회",
    description="등록된 모든 카테고리를 조회합니다."
)
async def get_all_categories(
    db: Session = Depends(get_db)
) -> ResponseBase[List[CategoryResponse]]:
    """
    전체 카테고리 목록 조회
    - 각 카테고리의 도서 개수 포함
    """
    try:
        categories = CategoryService.get_all_categories(db)
        return ResponseBase(
            status="success",
            data=[CategoryResponse.from_orm(cat) for cat in categories],
            message=f"총 {len(categories)}개의 카테고리가 조회되었습니다"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": "서버 오류가 발생했습니다"}
        )