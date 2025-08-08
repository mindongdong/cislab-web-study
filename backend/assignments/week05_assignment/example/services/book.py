# app/services/book_service.py
"""
Book 서비스 계층
- 도서 관련 복잡한 비즈니스 로직 처리
- 검색, 필터링, 페이지네이션 구현
"""
from typing import List, Optional, Tuple
from datetime import date
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import and_, or_, func
from sqlalchemy.exc import IntegrityError
from app.models.book import Book
from app.models.category import Category
from app.schemas.book import (
    BookCreate, BookUpdate, StockUpdateRequest, BookSearchParams
)
from app.utils.exceptions import (
    NotFoundException, DuplicateException, 
    InsufficientStockException, InvalidOperationException
)

class BookService:
    """도서 서비스 클래스"""
    
    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> Book:
        """
        도서 생성
        - 카테고리 존재 여부 확인
        - ISBN 중복 체크
        """
        # 카테고리 유효성 검증
        if book_data.category_id:
            category = db.query(Category).filter(
                Category.id == book_data.category_id
            ).first()
            if not category:
                raise NotFoundException("카테고리", book_data.category_id)
        
        try:
            db_book = Book(**book_data.dict())
            db.add(db_book)
            db.commit()
            db.refresh(db_book)
            
            # 카테고리 정보와 함께 반환
            return BookService.get_book_by_id(db, db_book.id)
        except IntegrityError as e:
            db.rollback()
            if "Duplicate entry" in str(e) or "UNIQUE constraint" in str(e):
                raise DuplicateException("ISBN", book_data.isbn)
            raise
    
    @staticmethod
    def get_all_books(
        db: Session, 
        params: BookSearchParams
    ) -> Tuple[List[Book], int]:
        """
        도서 목록 조회 (검색, 필터링, 페이지네이션)
        - 복잡한 쿼리 조건 처리
        - N+1 문제 해결을 위한 eager loading
        """
        # 기본 쿼리 - 카테고리 정보와 함께 조회
        query = db.query(Book).options(
            selectinload(Book.category)  # 별도 쿼리로 카테고리 정보 로드
        )
        
        # 검색 조건 적용 (제목 또는 저자명)
        if params.search:
            search_term = f"%{params.search}%"
            query = query.filter(
                or_(
                    Book.title.like(search_term),
                    Book.author.like(search_term)
                )
            )
        
        # 카테고리 필터
        if params.category_id:
            query = query.filter(Book.category_id == params.category_id)
        
        # 가격 범위 필터
        if params.min_price is not None:
            query = query.filter(Book.price >= params.min_price)
        if params.max_price is not None:
            query = query.filter(Book.price <= params.max_price)
        
        # 전체 개수 조회 (페이지네이션용)
        total = query.count()
        
        # 페이지네이션 적용
        offset = (params.page - 1) * params.size
        books = query.offset(offset).limit(params.size).all()
        
        # 카테고리명 추가
        for book in books:
            if book.category:
                book.category_name = book.category.name
        
        return books, total
    
    @staticmethod
    def get_book_by_id(db: Session, book_id: int) -> Book:
        """
        특정 도서 상세 조회
        - 카테고리 정보 포함
        """
        book = db.query(Book).options(
            joinedload(Book.category)  # JOIN을 통한 카테고리 정보 로드
        ).filter(Book.id == book_id).first()
        
        if not book:
            raise NotFoundException("도서", book_id)
        
        # 카테고리명 추가
        if book.category:
            book.category_name = book.category.name
        
        return book
    
    @staticmethod
    def update_book(
        db: Session, 
        book_id: int, 
        book_data: BookUpdate
    ) -> Book:
        """
        도서 정보 수정
        - 부분 업데이트 지원
        - ISBN 중복 체크
        """
        book = BookService.get_book_by_id(db, book_id)
        
        # 카테고리 변경 시 유효성 검증
        if book_data.category_id is not None:
            if book_data.category_id:  # None이 아니고 0이 아닌 경우
                category = db.query(Category).filter(
                    Category.id == book_data.category_id
                ).first()
                if not category:
                    raise NotFoundException("카테고리", book_data.category_id)
        
        # 변경사항 적용
        update_data = book_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        
        try:
            db.commit()
            db.refresh(book)
            return BookService.get_book_by_id(db, book_id)
        except IntegrityError:
            db.rollback()
            if book_data.isbn:
                raise DuplicateException("ISBN", book_data.isbn)
            raise
    
    @staticmethod
    def delete_book(db: Session, book_id: int) -> dict:
        """도서 삭제"""
        book = BookService.get_book_by_id(db, book_id)
        book_title = book.title
        
        db.delete(book)
        db.commit()
        
        return {"message": f"도서 '{book_title}'이(가) 삭제되었습니다"}
    
    @staticmethod
    def update_stock(
        db: Session, 
        book_id: int, 
        stock_update: StockUpdateRequest
    ) -> Book:
        """
        재고 수량 변경
        - 트랜잭션 처리로 동시성 문제 방지
        - 음수 재고 방지
        """
        # 행 잠금(row lock)을 통한 동시성 제어
        book = db.query(Book).filter(
            Book.id == book_id
        ).with_for_update().first()  # SELECT ... FOR UPDATE
        
        if not book:
            raise NotFoundException("도서", book_id)
        
        # 재고 계산
        if stock_update.operation == "add":
            book.stock_quantity += stock_update.quantity
        elif stock_update.operation == "subtract":
            if book.stock_quantity < stock_update.quantity:
                raise InsufficientStockException(
                    book.stock_quantity, 
                    stock_update.quantity
                )
            book.stock_quantity -= stock_update.quantity
        else:
            raise InvalidOperationException(
                f"유효하지 않은 작업: {stock_update.operation}"
            )
        
        db.commit()
        db.refresh(book)
        
        return BookService.get_book_by_id(db, book_id)