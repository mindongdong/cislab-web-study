from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer,VARCHAR, DATE, TIMESTAMP, String, func, ForeignKey, Text
from sqlalchemy.orm import relationship
import sys,os
sys.path.append(os.path.join(os.path.dirname((__file__),'..')))

Base = declarative_base()

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(13),unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, default=0, nullable=False)
    published_date = Column(DATE)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"),nullable=False )
    
    category = relationship("Category", back_populates="book")
    
class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    
    book = relationship("Book", back_populates="category", cascade = "all, delete")
    