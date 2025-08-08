# app/services/category_service.py
"""
Category 서비스 계층
- 카테고리 관련 비즈니스 로직 처리
- 데이터베이스 트랜잭션 관리
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.exceptions import NotFoundException, DuplicateException

class CategoryService:
    """카테고리 서비스 클래스"""
    
    @staticmethod
    def create_category(db: Session, category_data: CategoryCreate) -> Category:
        """
        카테고리 생성
        - 중복 체크 및 트랜잭션 처리
        """
        try:
            # 새 카테고리 객체 생성
            db_category = Category(**category_data.dict())
            db.add(db_category)
            db.commit()
            db.refresh(db_category)  # ID 등 자동 생성 필드 갱신
            return db_category
        except IntegrityError as e:
            db.rollback()
            # Unique 제약 조건 위반 시 (중복된 이름)
            if "Duplicate entry" in str(e) or "UNIQUE constraint" in str(e):
                raise DuplicateException("카테고리명", category_data.name)
            raise
    
    @staticmethod
    def get_all_categories(db: Session) -> List[Category]:
        """
        전체 카테고리 조회
        - 도서 개수 정보와 함께 조회 (N+1 문제 해결)
        """
        categories = db.query(Category).options(
            joinedload(Category.books)  # 한 번의 쿼리로 관련 도서 정보도 조회
        ).all()
        
        # 각 카테고리의 도서 개수 계산
        for category in categories:
            category.book_count = len(category.books)
        
        return categories
    
    @staticmethod
    def get_category_by_id(db: Session, category_id: int) -> Category:
        """
        특정 카테고리 조회
        - 존재하지 않으면 예외 발생
        """
        category = db.query(Category).filter(
            Category.id == category_id
        ).first()
        
        if not category:
            raise NotFoundException("카테고리", category_id)
        
        return category
    
    @staticmethod
    def update_category(
        db: Session, 
        category_id: int, 
        category_data: CategoryUpdate
    ) -> Category:
        """
        카테고리 수정
        - 부분 업데이트 지원 (PATCH)
        """
        category = CategoryService.get_category_by_id(db, category_id)
        
        # 변경할 데이터만 업데이트
        update_data = category_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(category, field, value)
        
        try:
            db.commit()
            db.refresh(category)
            return category
        except IntegrityError:
            db.rollback()
            raise DuplicateException("카테고리명", category_data.name)
    
    @staticmethod
    def delete_category(db: Session, category_id: int) -> dict:
        """
        카테고리 삭제
        - cascade 옵션에 따라 연관 도서도 함께 삭제
        """
        category = CategoryService.get_category_by_id(db, category_id)
        
        # 삭제 전 정보 저장 (응답용)
        category_name = category.name
        
        db.delete(category)
        db.commit()
        
        return {"message": f"카테고리 '{category_name}'이(가) 삭제되었습니다"}
