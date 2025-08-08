from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional


from layers.connection import get_db
from layers.DTO import BookModel,CategoryModel, ListBookModel
from layers.service import read_all_book_list, read_book_by_id,create_book,create_category,update_book,delete_book, update_stock

app = FastAPI()

@app.get("/")
def home():
    return {"operation": "succeded", "page": "home"}

#도서 전체 목록 조회
@app.get("/books", response_model = List[BookModel])
def read_all_books(session : Session = Depends(get_db),
                   search: Optional[str] = None,
                   category_id : Optional[int] = None,
                   min_price : Optional[int] = None,
                   max_price : Optional[int] = None,
                   page : int=Query(1, ge =1),
                   size : int = Query(10, ge=1)):
    return read_all_book_list(session=session,
                              search = search,
                              category_id=category_id,
                              min_price=min_price,
                              max_price=max_price,
                              page=page,
                              size=size)
    
#도서 id로 상세조회
@app.get("/books/{book_id}", response_model=BookModel)
def read_id_book( book_id : int, session : Session = Depends(get_db)):
    results = read_book_by_id(book_id, session=session)
    return results

#전체 카테고리 목록 조회
@app.get("/categories", response_model=List[CategoryModel])
def read_all_category(session : Session = Depends(get_db)):
    results = read_all_category(session=session)
    return results

#새 도서 등록
@app.post("/books", response_model=BookModel)
def post_new_book(book : BookModel , session : Session = Depends(get_db)):
    results = create_book(session=session, book_data=book)
    return results

#새 카테고리 등록
@app.post("/categories", response_model=CategoryModel)
def post_new_category(category : CategoryModel, session : Session = Depends(get_db)):
    results = create_category(session=session,category_data=category)
    return results
    

#도서 정보 수정
@app.patch("/books/{book_id}", response_model=BookModel) 
def update_id_book(book_id : int, book : BookModel, session : Session = Depends(get_db)):
    results = update_book(session = session, update_data=book)
    return results

#도서 삭제
@app.delete("/books/{book_id}", response_model=BookModel)
def delete_id_book(book_id : int ,session : Session =Depends(get_db)):
    results = delete_book(book_id=book_id, session=session)
    return results

#재고관리
@app.patch("/books/{book_id}/stock", response_model = BookModel)
def stock_book(book_id : int, payload : dict, session : Session = Depends(get_db)):
    results = update_stock(book_id=book_id, session=session, payload=payload)
    return results
    
        


