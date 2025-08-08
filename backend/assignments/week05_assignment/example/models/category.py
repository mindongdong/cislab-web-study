"""
Category 모델 정의
- 도서 카테고리를 관리하는 테이블
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Category(Base):
    """카테고리 ORM 모델"""
    __tablename__ = "categories"
    
    # Primary Key - 자동 증가
    id = Column(Integer, primary_key=True, index=True)
    
    # 카테고리명 - 고유값으로 중복 방지
    name = Column(String(50), nullable=False, unique=True, index=True)
    
    # 설명 - 선택적 필드
    description = Column(Text, nullable=True)
    
    # 생성 시간 - server_default로 DB 레벨에서 자동 설정
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    
    # 관계 설정 - 카테고리에 속한 도서들
    # back_populates: 양방향 관계 설정
    # cascade: 카테고리 삭제 시 연관 도서 처리 방식
    books = relationship(
        "Book", 
        back_populates="category",
        cascade="all, delete-orphan"  # 카테고리 삭제 시 도서도 삭제
    )
    
    def __repr__(self):
        """디버깅을 위한 표현 문자열"""
        return f"<Category(id={self.id}, name='{self.name}')>"
