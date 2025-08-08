"""
Book API 엔드포인트
- 복잡한 비즈니스 로직과 다양한 쿼리 파라미터 처리
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.book import (
    BookCreate, BookUpdate, BookResponse, 
    StockUpdateRequest, BookSearchParams
)
from app.schemas.common import ResponseBase, PaginatedResponse, PaginationMeta
from app.services.book_service import BookService
from app.utils.exceptions import BusinessException
import math

router = APIRouter(
    prefix="/books",
    tags=["Books"],
    responses={
        404: {"description": "도서를 찾을 수 없습니다"},
        400: {"description": "잘못된 요청입니다"}
    }
)

@router.post(
    "",
    response_model=ResponseBase[BookResponse],
    status_code=status.HTTP_201_CREATED,
    summary="도서 등록",
    description="새로운 도서를 등록합니다. ISBN은 13자리 숫자여야 합니다."
)
async def create_book(
    book_data: BookCreate,
    db: Session = Depends(get_db)
) -> ResponseBase[BookResponse]:
    """
    도서 생성 엔드포인트
    - ISBN 중복 체크
    - 카테고리 존재 여부 확인
    """
    try:
        book = BookService.create_book(db, book_data)
        return ResponseBase(
            status="success",
            data=BookResponse.from_orm(book),
            message="도서가 성공적으로 등록되었습니다"
        )
    except BusinessException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"status": "error", "message": e.message}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": f"서버 오류: {str(e)}"}
        )

@router.get(
    "",
    response_model=PaginatedResponse[List[BookResponse]],
    summary="도서 목록 조회",
    description="도서 목록을 조회합니다. 검색, 필터링, 페이지네이션을 지원합니다."
)
async def get_books(
    search: Optional[str] = Query(None, description="검색어 (제목/저자)"),
    category_id: Optional[int] = Query(None, gt=0, description="카테고리 ID"),
    min_price: Optional[int] = Query(None, ge=0, description="최소 가격"),
    max_price: Optional[int] = Query(None, ge=0, description="최대 가격"),
    page: int = Query(1, gt=0, description="페이지 번호"),
    size: int = Query(10, gt=0, le=100, description="페이지 크기"),
    db: Session = Depends(get_db)
) -> PaginatedResponse[List[BookResponse]]:
    """
    도서 목록 조회 엔드포인트
    - 검색: 제목 또는 저자명에 키워드 포함
    - 필터링: 카테고리, 가격대
    - 페이지네이션: 기본 10개씩
    
    쿼리 파라미터 예시:
    - /books?search=파이썬
    - /books?category_id=1&min_price=10000&max_price=50000
    - /books?page=2&size=20
    """
    try:
        # 검색 파라미터 객체 생성
        params = BookSearchParams(
            search=search,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            page=page,
            size=size
        )
        
        # 서비스 호출
        books, total = BookService.get_all_books(db, params)
        
        # 페이지네이션 메타 정보 계산
        total_pages = math.ceil(total / size) if total > 0 else 0
        
        return PaginatedResponse(
            status="success",
            data=[BookResponse.from_orm(book) for book in books],
            message=f"총 {total}개 중 {len(books)}개의 도서가 조회되었습니다",
            meta=PaginationMeta(
                page=page,
                size=size,
                total=total,
                total_pages=total_pages
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": f"서버 오류: {str(e)}"}
        )

@router.get(
    "/{book_id}",
    response_model=ResponseBase[BookResponse],
    summary="도서 상세 조회",
    description="특정 도서의 상세 정보를 조회합니다."
)
async def get_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> ResponseBase[BookResponse]:
    """
    도서 상세 조회 엔드포인트
    - 카테고리 정보 포함
    """
    try:
        book = BookService.get_book_by_id(db, book_id)
        return ResponseBase(
            status="success",
            data=BookResponse.from_orm(book),
            message="도서 정보가 조회되었습니다"
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

@router.patch(
    "/{book_id}",
    response_model=ResponseBase[BookResponse],
    summary="도서 정보 수정",
    description="도서 정보를 부분적으로 수정합니다."
)
async def update_book(
    book_id: int,
    book_data: BookUpdate,
    db: Session = Depends(get_db)
) -> ResponseBase[BookResponse]:
    """
    도서 정보 수정 엔드포인트
    - PATCH 메서드로 부분 업데이트 지원
    - 변경하고자 하는 필드만 전송
    """
    try:
        book = BookService.update_book(db, book_id, book_data)
        return ResponseBase(
            status="success",
            data=BookResponse.from_orm(book),
            message="도서 정보가 성공적으로 수정되었습니다"
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

@router.delete(
    "/{book_id}",
    response_model=ResponseBase[dict],
    summary="도서 삭제",
    description="도서를 삭제합니다."
)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
) -> ResponseBase[dict]:
    """
    도서 삭제 엔드포인트
    - 물리적 삭제 수행
    """
    try:
        result = BookService.delete_book(db, book_id)
        return ResponseBase(
            status="success",
            data=result,
            message="도서가 성공적으로 삭제되었습니다"
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

@router.patch(
    "/{book_id}/stock",
    response_model=ResponseBase[BookResponse],
    summary="재고 수량 변경",
    description="도서의 재고를 추가하거나 차감합니다."
)
async def update_stock(
    book_id: int,
    stock_update: StockUpdateRequest,
    db: Session = Depends(get_db)
) -> ResponseBase[BookResponse]:
    """
    재고 관리 엔드포인트
    - 재고 추가/차감 기능
    - 음수 재고 방지
    - 트랜잭션 처리로 동시성 문제 해결
    
    요청 예시:
    {
        "quantity": 10,
        "operation": "add"  // 또는 "subtract"
    }
    """
    try:
        book = BookService.update_stock(db, book_id, stock_update)
        
        operation_msg = "추가" if stock_update.operation == "add" else "차감"
        return ResponseBase(
            status="success",
            data=BookResponse.from_orm(book),
            message=f"재고가 {stock_update.quantity}개 {operation_msg}되었습니다. 현재 재고: {book.stock_quantity}개"
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