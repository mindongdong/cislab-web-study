"""
Book 모델 정의
- 도서 정보를 관리하는 핵심 테이블
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Book(Base):
    """도서 ORM 모델"""
    __tablename__ = "books"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # 도서 정보 필드들
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    
    # ISBN - 13자리 고유값
    isbn = Column(String(13), unique=True, nullable=False, index=True)
    
    # 가격과 재고
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    
    # 출간일
    published_date = Column(Date, nullable=True)
    
    # 타임스탬프 필드들
    # server_default: INSERT 시 자동 설정
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # onupdate: UPDATE 시 자동 갱신
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Foreign Key - 카테고리 관계
    category_id = Column(
        Integer, 
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True  # 조인 성능 최적화를 위한 인덱스
    )
    
    # 관계 설정
    category = relationship("Category", back_populates="books")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', isbn='{self.isbn}')>"