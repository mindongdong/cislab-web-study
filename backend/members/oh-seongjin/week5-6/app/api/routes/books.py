from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, and_, update, delete
from sqlalchemy.orm import Session, joinedload

from app.api.deps import get_db
from app.models import Book, Category
from app.schemas.book import BookCreate, BookUpdate, StockUpdate, BookOut
from app.utils.responses import make_response

router = APIRouter(prefix="/books", tags=["books"])

@router.post("", response_model=dict)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    if payload.category_id is not None:
        exists = db.execute(
            select(Category.id).where(Category.id == payload.category_id)
        ).scalar_one_or_none()
        if exists is None:
            raise HTTPException(status_code=404, detail="category not found")
    book = Book(**payload.model_dump())
    db.add(book)
    try:
        db.commit()
        db.refresh(book)
    except Exception as e:
        db.rollback()
        if "UNIQUE" in str(e).upper() and "ISBN" in str(e).upper():
            raise HTTPException(status_code=400, detail="ISBN already exists")
        raise
    return make_response("success", BookOut.model_validate(book), "registered successfully")

@router.get("", response_model=dict)
def list_books(
    search: str | None = None,
    category_id: int | None = None,
    min_price: int | None = Query(default=None, ge=0),
    max_price: int | None = Query(default=None, ge=0),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    filters = []
    if search:
        filters.append((Book.title.contains(search)) | (Book.author.contains(search)))
    if category_id is not None:
        filters.append(Book.category_id == category_id)
    if min_price is not None:
        filters.append(Book.price >= min_price)
    if max_price is not None:
        filters.append(Book.price <= max_price)

    where_clause = and_(*filters) if filters else None

    count_stmt = select(func.count()).select_from(Book)
    if where_clause is not None:
        count_stmt = count_stmt.where(where_clause)
    total = db.execute(count_stmt).scalar_one()

    query = select(Book).options(joinedload(Book.category))
    if where_clause is not None:
        query = query.where(where_clause)
    items = db.execute(
        query.offset((page - 1) * size).limit(size)
    ).scalars().all()

    data = [BookOut.model_validate(b) for b in items]
    meta = {"page": page, "size": size, "total": total}
    return make_response("success", data, "book list retrieved successfully", meta)

@router.get("/{book_id}", response_model=dict)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.execute(
        select(Book).options(joinedload(Book.category)).where(Book.id == book_id)
    ).scalar_one_or_none()
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    return make_response(BookOut.model_validate(book))

@router.patch("/{book_id}", response_model=dict)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    to_update = payload.model_dump(exclude_unset=True)
    if not to_update:
        raise HTTPException(status_code=400, detail="no data to update")

    exists = db.execute(select(Book.id).where(Book.id == book_id)).scalar_one_or_none()
    if exists is None:
        raise HTTPException(status_code=404, detail="book not found")

    if "category_id" in to_update and to_update["category_id"] is not None:
        cat_ok = db.execute(
            select(Category.id).where(Category.id == to_update["category_id"])
        ).scalar_one_or_none()
        if cat_ok is None:
            raise HTTPException(status_code=404, detail="category not found")

    to_update["updated_at"] = datetime.utcnow()
    stmt = update(Book).where(Book.id == book_id).values(**to_update)
    db.execute(stmt)
    db.commit()

    book = db.execute(
        select(Book).options(joinedload(Book.category)).where(Book.id == book_id)
    ).scalar_one()
    return make_response("success", BookOut.model_validate(book), "book updated successfully")

@router.delete("/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    exists = db.execute(select(Book.id).where(Book.id == book_id)).scalar_one_or_none()
    if exists is None:
        raise HTTPException(status_code=404, detail="book not found")

    db.execute(delete(Book).where(Book.id == book_id))
    db.commit()
    return make_response("success", None, "book deleted successfully")

@router.patch("/{book_id}/stock", response_model=dict)
def update_stock(book_id: int, payload: StockUpdate, db: Session = Depends(get_db)):
    stock = db.execute(select(Book.stock_quantity).where(Book.id == book_id)).scalar_one_or_none()
    if stock is None:
        raise HTTPException(status_code=404, detail="book not found")

    if payload.operation == "add":
        new_stock = stock + payload.quantity
    else:
        if stock - payload.quantity < 0:
            raise HTTPException(status_code=400, detail="out of stock")
        new_stock = stock - payload.quantity

    stmt = update(Book).where(Book.id == book_id).values(
        stock_quantity=new_stock, updated_at=datetime.utcnow()
    )
    db.execute(stmt)
    db.commit()
    return make_response("success", {"id": book_id, "stock_quantity": new_stock}, "stock updated successfully")
