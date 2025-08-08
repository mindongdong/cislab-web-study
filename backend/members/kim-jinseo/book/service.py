from sqlalchemy import select, or_
from sqlalchemy.orm import Session, joinedload
from layers.orm import Book,Category
from typing import List
from fastapi import HTTPException

from layers.DTO import BookModel,CategoryModel

# 고찰1 : scalar() 와 get()... get()은 PK값으로만 조회 가능하지만, 캐시로 접근하기 때문에 훨씬 빠르다.
# 고찰2 : sqlalchemy의 get(), dict의 get()

#전체 도서 목록 리스트 조회
def read_all_book_list(session:Session, search=None, category_id = None, min_price = None, max_price = None, page=1,size=10 ):
    stmt = select(Book).options(joinedload(Book.category))
    
    if search:
        stmt = stmt.where(or_(Book.title.like(f"%{search}%"), Book.author.like(f"%{search}%")))
    if category_id:
        stmt = stmt.where(Book.category_id == category_id)
    if min_price is not None:
        stmt= stmt.where(Book.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Book.price <= max_price)
    
    stmt = stmt.offset((page - 1) * size).limit(size)
        
    books = session.scalars(select(Book)).all() #list()는 느리고, scalars()는 Book객체만 추출하므로, list()대신 .all()이 일반적이다.
    return books
    
    
#id조회 도서목록 조회
def read_book_by_id(book_id : int, session : Session):
    #book = session.scalar(select(Book).where(Book.id==book_id))
    book = session.get(Book,book_id) #캐시로 접근하기 때문에 더 빠르다. 어차피 PK로 접근 할거면
    if not book:
        raise HTTPException(status_code=404, detail='Not Found')
    return book

#전체 카테고리 목록 리스트 조회
def read_all_category_list(session : Session)
    return session.scalars(select(Category)).all()

#새 도서 등록
def create_book(session : Session , book_data : BookModel): #데이터베이스의 데이터를 가지고 와야 하기 때문에, 유효성 검사진행
                                                            # 단순한 조회 에서는 단순 존재 여부만 확인하면 되기때문에, 유효성 검사 안했음.
    #isbn중복검사
    isbn_exist = session.scalar(select(Book).where(Book.isbn == book_data.isbn))
    if isbn_exist:
        raise HTTPException(status_code=400, detail = "isbn already exists")
    
    new_book = Book(**book_data.model_dump(exclude_unset=True)) #ORM Book객체 생성
                                                                #클라이언트가 입력한 book_data의 유효성 검사후 dict로 변환한다.
                                                                #exclude_unset=True: 실제로 입력된 필드만 dict에 포함.
    session.add(new_book)
    session.commit() #실제 데이터베이스에 저장
    session.refresh(new_book) #db에서 new_book을 다시 조회해서 최신 상태로 갱신해줌.(db에서 최신 계산 상태를 즉시 반영)
    return new_book

#새 카테고리 등록
def create_category(session : Session, category_data : CategoryModel):
    #name중복검사
    name_exist = session.scalar(select(Category).where(Category.name==category_data.name))
    if name_exist:
        raise HTTPException(status_code=400, detail="category name is already exists")
    
    new_category = Category(**category_data.model_dump(exclude_unset=True))
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category

#도서 정보 수정
def update_book(book_id : int , session : Session , update_data : BookModel): 
    #book_exist = session.scalar(select(Book).where(Book.id==update_data.id))
    book_exist = session.get(Book, book_id) #실존 확인용 book_exist
    if not book_exist:
        raise HTTPException(status_code=404, detail='not found')
    
    updated_book = Book(update_data.model_dump(exclude_unset=True))
    for column,value in updated_book.items():
        setattr(book, column, value) #ORM 테이블 Book의 해당 속성을 동적으로 수정
    session.commit()
    session.refresh(updated_book)
    return updated_book

#도서 삭제
def delete_book(book_id : int, session : Session): #, delete_data : BookModel
    #deleted_data = session.scalar(select(Book).where(Book.id==delete_data.id))
    deleted_data = session.get(Book, book_id) #이 book이 삭제될 book
    if not deleted_data:
        raise HTTPException(status_code=404, detail='not Found')

    session.delete(deleted_data)
    session.commit()
    return {'삭제가 완료 되었습니다.'}

#재고관리
def update_stock(session : Session , book_id : int, payload: dict):
    #book_exist = session.scalar(select(Book).where(Book.id==stock_data.id))
    book = session.get(Book,book_id)
    if not book:
        raise HTTPException(status_code=404, detail = "Not Found")
    
    quantity = payload.get("quantity") # dict의 get()메서드
    operation = payload.get("operation")
    
    if quantity is None or operation is not ("add","substract"):
        raise HTTPException(status_code=400,detail = "No payload")
    
    if operation == "add":
        book.stock_quantity +=quantity
    elif operation == "substract":
        if book.stock_quantity < quantity:
            raise HTTPException(status_code=400, detail = "it will be zero")        
        book.stock_quantity -=quantity
    
    session.commit()
    session.refresh(book)
    retrun book
    
    