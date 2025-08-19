import pytest
from layer.orm import Book, Category

#홈화면 테스트
def test_health(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"operation": "succeded", "page": "home"}





#빈 목록일 때
def test_get_books_empty(test_client):
    response = test_client.get("/books")
    assert response.status_code == 200
    assert response.json() == []





# 샘플 도서 1권 추가후에 데이터 있을때 정상 조회/ 검색조회
def test_get_books(test_client, test_db, sample_category):
    book = Book(
        title="python programming",
        author="jskim",
        isbn="6",
        price=25000,
        stock_quantity=5,
        category_id=sample_category.id,
    )
    test_db.add(book)
    test_db.commit()

    #데이터가 있을 때 정상 조회
    response = test_client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list) #리스트인지 보장하는 안전장치
    assert len(data) == 1
    assert data[0]["title"] == "python programming"

    #검색: 제목에 "python" 포함
    response = test_client.get("/books?search=python")
    assert response.status_code == 200
    titles = [item["title"] for item in response.json()]
    assert "python programming" in titles






#GET /books/{book_id} 테스트 - 정상조회/ 존재하지 않는 id조회/ 잘못된 id형식
def test_get_book_by_id(test_client, test_db):
    
    # 샘플 카테고리 생성
    category = Category(name="deep learning")
    test_db.add(category)
    test_db.commit()
    
    #샘플 책 생성
    book = Book(
    title="python",
    author="dwlee",
    isbn="11",
    price=30000,
    stock_quantity=10,
    category_id=category.id,
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)
    
    #정상 조회
    response = test_client.get(f"/books/{book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book.id
    assert data["title"] == "python"
    assert data["isbn"] == "11"
    
    #존재하지 않는 ID 조회
    response = test_client.get("/books/111111111111")  # 없는 ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"
    
    #잘못된 ID 형식 (문자열)
    response = test_client.get("/books/abc")
    assert response.status_code == 422 
    errors = response.json()["detail"]
    assert errors[0]["type"] == "fail...not int"  # 정수 변환 실패
    
    
    
    
    
#POST /books 테스트 - 정상생성 / 중복isbn
def test_create_book(test_client, test_db):
    
    # 샘플 카테고리 생성
    category = Category(name="deep learning")
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)

    #정상 생성
    new_book = {
        "title": "CNN",
        "author": "jskim",
        "isbn": "21",
        "price": 25000,
        "stock_quantity": 5,
        "category_id": category.id,
    }
    response = test_client.post("/books", json=new_book)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "CNN"
    assert data["isbn"] == "21"
    assert data["category"]["id"] == category.id

    #중복 ISBN
    response = test_client.post("/books", json=new_book)
    assert response.status_code == 400 
    assert response.json()["detail"] == "ISBN already exists"


#PATCH /books/{book_id} 테스트 - 정상 수정, 존재하지 않는 도서 수정시도
def test_patch_book(test_client, test_db):
    
    # 샘플 카테고리 생성
    category = Category(name="robotics")
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    
    #샘플 책 생성
    book = Book(
        title="introduction robotics",
        author="jskim",
        isbn="3",
        price=20000,
        stock_quantity=10,
        category_id=category.id,
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)
    
    #정상 수정
    patch_data = {"price": 22000, "stock_quantity": 15}
    response = test_client.patch(f"/books/{book.id}", json=patch_data)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 22000
    assert data["stock_quantity"] == 15
    
    #존재하지 않는 도서 수정 시도
    response = test_client.patch("/books/11111", json={"price": 30000})
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
    
    
    


#DELETE /books/{book_id} 테스트 - 정상삭제, 존재하지 않는 도서 삭제 시도
def test_delete_book(test_client, test_db):
    
    # 샘플 카테고리 생성
    category = Category(name="robotics")
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)

    #샘플 책 생성
    book = Book(
        title="introduction robotics",
        author="jskim",
        isbn="11",
        price=15000,
        stock_quantity=5,
        category_id=category.id,
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)
    
    #정상 삭제
    response = test_client.delete(f"/books/{book.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
    
    #존재하지 않는 도서 삭제 시도
    response = test_client.delete("/books/1111")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
    
    
    
    
#PATCH /books/{book_id}/stock -재고추가, 삭제
def test_stock_add_and_substract(test_client, test_db):
    
    #카테고리 생성
    category = Category(name="hardware", description="about hardware")
    test_db.add(category)
    test_db.commit()
    test_db.refresh(category)
    
    #책 생성
    book = Book(
        title="computer hardware",
        author="jskim",
        isbn="111111",
        price=10000,
        stock_quantity=10,
        category_id=category.id,
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)
    
    #재고 추가 (operation: "add")
    response = test_client.patch(f"/books/{book.id}/stock", json={"operation": "add", "quantity": 5})
    assert response.status_code == 200
    body = response.json()
    assert body["stock_quantity"] == 15  # 10 + 5
    
    #재고 차감 (주의: 구현에선 "substract"로 철자)
    response = test_client.patch(f"/books/{book.id}/stock", json={"operation": "substract", "quantity": 3})
    assert response.status_code == 200
    body = response.json()
    assert body["stock_quantity"] == 12  # 15 - 3
    



#Category API 테스트

#빈 목록일 때
def test_get_categories_empty(test_client):
    response = test_client.get("/categories")
    assert response.status_code == 200
    assert response.json() == []


#POST /categories 테스트 -정상생성, 중복이름으로 재시도
def test_post_category_and_duplicate(test_client, test_db):
    
    #정상 생성
    payload = {
        "id": 0,
        "name": "C++",
        "description": "about C++",
        "created_at": "2025-08-18T00:00:00",  # DTO에 created_at 필드가 있어서 넣어줌
    }
    response = test_client.post("/categories", json=payload)
    assert response.status_code ==200
    body = response.json()
    assert body["name"] == "C++"
    
    #중복 이름
    dup = {
        "id": 0,
        "name": "C++",         # 같은 이름으로 재요청
        "description": "Duplicate",
        "created_at": "2025-08-18T00:00:00",
    }
    response = test_client.post("/categories", json=dup)
    assert response.status_code == 400
    assert response.json() == {"detail": "category name is already exists"}
