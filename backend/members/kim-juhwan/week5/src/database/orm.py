from schema.request import CreateBookRequest, CreateCategoryRequest
from sqlalchemy import Boolean, Column, Integer, String, CHAR, Text, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TIMESTAMP

Base = declarative_base()


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(CHAR(13), nullable=True, unique=True)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=True, default=0)
    published_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    category = relationship("Category", back_populates="books")

    def __repr__(self):
        return f"Book(id={self.id}, contents={self.title}, is_done={self.author}, isbn={self.isbn}, \
        price = {self.price}, stock_quantity={self.stock_quantity}, published_date={self.published_date}, \
        created_at={self.created_at}, updated_at={self.updated_at}, category_id={self.category_id})"

    @classmethod
    def create(cls, request: CreateBookRequest) -> "Book":
        return cls(
            title=request.title,
            author=request.author,
            isbn=request.isbn,       # None이어도 DB 컬럼이 nullable이므로 OK
            price=request.price,
            stock_quantity=request.stock_quantity,
            published_date=request.published_date,
            category_id=request.category_id
        )

    # def sold(self) -> "Book":
    #     if self.stock_quantity > 0:
    #         self.stock_quantity -= 1
    #
    #     return self
    #
    # def added(self) -> "Book":
    #     self.stock_quantity += 1
    #
    #     return self


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    books = relationship("Book", back_populates="category")

    def __repr__(self):
        return f"Category(id={self.id}, name={self.name}, description={self.description}, \
        created_at={self.created_at}, books={self.books})"

    @classmethod
    def create(cls, request: CreateCategoryRequest) -> "Category":
        return cls(
            name=request.name,
            description=request.description
        )