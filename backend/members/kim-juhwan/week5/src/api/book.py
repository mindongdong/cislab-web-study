from typing import List

from database.connection import get_db
from database.orm import Book
from database.repository import get_books, get_book_by_book_id, create_book, update_book, delete_book, update_book_stock
from fastapi import Depends, HTTPException, APIRouter, Query

from schema.request import CreateBookRequest, UpdateBookRequest, UpdateStockRequest
from schema.response import BookListSchema, BookSchema
from sqlalchemy.orm import Session

router = APIRouter(prefix="/books")

@router.get("", status_code=200)
def get_books_handler(
        order: str | None = None,
        session: Session = Depends(get_db),
        # 검색, 필터링, 페이지네이션 파라미터 추가
        search: str | None = Query(None, description="제목 또는 저자명 검색"),
        category_id: int | None = Query(None, description="카테고리 ID 필터링"),
        min_price: int | None = Query(None, description="최소 가격 필터링"),
        max_price: int | None = Query(None, description="최대 가격 필터링"),
        page: int = Query(1, ge=1, description="페이지 번호"),
        size: int = Query(10, ge=1, le=100, description="페이지 당 항목 수"),
) -> BookListSchema:

    books: List[Book] = get_books(
        session=session,
        page=page,
        size=size,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
    )

    if order and order.upper() == "DESC":
        return BookListSchema(
            books=[BookSchema.from_orm(book) for book in books[::-1]]
        )
    return BookListSchema(
        books=[BookSchema.from_orm(book) for book in books]
    )


@router.get("/{book_id}", status_code=200)
def get_book_handler(
        book_id: int,
        session: Session = Depends(get_db),
) -> BookSchema:
    book: Book | None = get_book_by_book_id(session=session, book_id=book_id)
    if book:
        return BookSchema.from_orm(book)
    raise HTTPException(status_code=404, detail="Book Not Found")


@router.post("", status_code=201)
def create_book_handler(
        request: CreateBookRequest,
        session: Session = Depends(get_db),
) -> BookSchema:
    book: Book = Book.create(request=request) # id=None
    book: Book = create_book(session=session, book=book) # id=int
    return BookSchema.from_orm(book)


@router.patch("/{book_id}", status_code=200)
def update_book_handler(
    book_id: int,
    request: UpdateBookRequest,
    # price: int = Body(..., embed=True),
    # stock_quantity: int = Body(..., embed=True),
    session: Session = Depends(get_db),
):
    book: Book | None = get_book_by_book_id(session=session, book_id=book_id)
    if book:
        # 비즈니스 로직 모두 repository의 update_book 함수에 위임
        updated_book = update_book(session=session, book=book, request=request)
        return BookSchema.from_orm(updated_book)
    raise HTTPException(status_code=404, detail="Book Not Found")


@router.patch("/{book_id}/stock", status_code=200)
def update_stock_handler(
        book_id: int,
        request: UpdateStockRequest,
        session: Session = Depends(get_db),
) -> BookSchema:
    book = get_book_by_book_id(session=session, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book Not Found")

    try:
        updated_book = update_book_stock(session=session, book=book, request=request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return BookSchema.from_orm(updated_book)

@router.delete("/{book_id}", status_code=204)
def delete_book_handler(
    book_id: int,
    session: Session = Depends(get_db),
):
    book: Book | None = get_book_by_book_id(session=session, book_id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="ToDo Not Found")
    # delete
    delete_book(session=session, book_id=book_id)
