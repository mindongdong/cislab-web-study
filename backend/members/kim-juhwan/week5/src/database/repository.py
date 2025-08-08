from typing import List

from schema.request import UpdateBookRequest, UpdateStockRequest
from sqlalchemy import select, delete, or_
from sqlalchemy.orm import Session
from database.orm import Book, Category


def get_books(
    session: Session,
    page: int,
    size: int,
    search: str | None = None,
    category_id: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
) -> List[Book]:
    query = select(Book)

    # 검색 기능 (제목 또는 저자)
    if search:
        query = query.where(
            or_(Book.title.contains(search), Book.author.contains(search))
        )
    # 필터링 기능 (카테고리, 가격)
    if category_id is not None:
        query = query.where(Book.category_id == category_id)
    if min_price is not None:
        query = query.where(Book.price >= min_price)
    if max_price is not None:
        query = query.where(Book.price <= max_price)
    # 페이지네이션
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)

    return list(session.scalars(query))

def get_book_by_book_id(session: Session, book_id: int) -> Book | None:
    return session.scalar(select(Book).where(Book.id == book_id))

def create_book(session: Session, book: Book) -> Book:
    session.add(instance=book)
    session.commit() # db save
    session.refresh(instance=book) # db read -> book_id
    return book

def update_book(session: Session, book: Book, request: UpdateBookRequest) -> Book:
    # request.dict(): Pydantic 모델 => 딕셔너리 변환
    # exclude_unset=True: 명시적으로 보낸 값만 딕셔너리에 포함
    update_data = request.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)  # setattr(object, name, value) => object.name = value

    session.add(instance=book)
    session.commit()
    session.refresh(instance=book)
    return book

def delete_book(session: Session, book_id: int) -> None:
    session.execute(delete(Book).where(Book.id == book_id))
    session.commit()


def update_book_stock(session: Session, book: Book, request: UpdateStockRequest) -> Book:
    if request.operation == "add":
        book.stock_quantity += request.quantity
    elif request.operation == "subtract":
        if book.stock_quantity < request.quantity:
            # 재고가 부족할 경우 예외 발생
            raise ValueError("재고가 없습니다.")
        book.stock_quantity -= request.quantity

    session.add(instance=book)
    session.commit()
    session.refresh(instance=book)
    return book

def get_categories(session: Session) -> List[Category]:
    return list(session.scalars(select(Category)))

def create_category(session: Session, category: Category) -> Category:
    session.add(instance=category)
    session.commit() # db save
    session.refresh(instance=category) # db read -> book_id
    return category