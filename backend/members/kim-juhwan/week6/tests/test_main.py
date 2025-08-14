from database.orm import Book
from pydantic.types import date
from schema.request import UpdateBookRequest
from unittest.mock import ANY


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}

def test_get_books(client, mocker):
    mock_books = [
        Book(id=1, title="Attention Is All You Need", author="Ashish Vaswani et al.", isbn="9780123456786", price=22000,
             stock_quantity=5, published_date="2017-06-12", created_at="2025-08-06T08:24:11",
             updated_at="2025-08-06T08:41:39", category_id=1),
        Book(id=2, title="Deep Residual Learning for Image Recognition", author="Kaiming He et al.",
             isbn="9780123456787",price=18000, stock_quantity=3, published_date="2015-12-10",
             created_at="2025-08-06T08:24:11", updated_at="2025-08-06T08:42:23", category_id=2),
    ]

    mocker.patch("api.book.get_books", return_value=mock_books)

    # order == ASC
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json() == {
        "books": [
            {
                "id": 1,
                "title": "Attention Is All You Need",
                "author": "Ashish Vaswani et al.",
                "isbn": "9780123456786",
                "price": 22000,
                "stock_quantity": 5,
                "published_date": "2017-06-12",
                "created_at": "2025-08-06T08:24:11",
                "updated_at": "2025-08-06T08:41:39",
                "category_id": 1
            },
            {
                "id": 2,
                "title": "Deep Residual Learning for Image Recognition",
                "author": "Kaiming He et al.",
                "isbn": "9780123456787",
                "price": 18000,
                "stock_quantity": 3,
                "published_date": "2015-12-10",
                "created_at": "2025-08-06T08:24:11",
                "updated_at": "2025-08-06T08:42:23",
                "category_id": 2
            },
        ]
    }
    # order == DESC
    response = client.get("/books?order=DESC")
    assert response.status_code == 200
    assert response.json() == {
        "books": [
            {
                "id": 2,
                "title": "Deep Residual Learning for Image Recognition",
                "author": "Kaiming He et al.",
                "isbn": "9780123456787",
                "price": 18000,
                "stock_quantity": 3,
                "published_date": "2015-12-10",
                "created_at": "2025-08-06T08:24:11",
                "updated_at": "2025-08-06T08:42:23",
                "category_id": 2
            },
            {
                "id": 1,
                "title": "Attention Is All You Need",
                "author": "Ashish Vaswani et al.",
                "isbn": "9780123456786",
                "price": 22000,
                "stock_quantity": 5,
                "published_date": "2017-06-12",
                "created_at": "2025-08-06T08:24:11",
                "updated_at": "2025-08-06T08:41:39",
                "category_id": 1
            }
        ]
    }
    # 빈 목록
    mocker.patch("api.book.get_books", return_value=[])
    response = client.get("/books")
    assert response.status_code == 200
    assert response.json()["books"] == []

    # 페이지네이션, 필터링, 검색 기능 통합 테스트
    mock_empty_books = mocker.patch("api.book.get_books", return_value=[])
    client.get("/books?page=2&size=5&category_id=1&min_price=100&max_price=1000&search=Test")
    mock_empty_books.assert_called_with(
        session=ANY,
        page=2,
        size=5,
        category_id=1,
        min_price=100,
        max_price=1000,
        search="Test"
    )

def test_get_book(client, mocker):
    # 200
    mocker.patch("api.book.get_book_by_book_id", return_value=
        Book(id=1, title="Attention Is All You Need", author="Ashish Vaswani et al.", isbn="9780123456786", price=22000,
             stock_quantity=5, published_date="2017-06-12", created_at="2025-08-06T08:24:11",
             updated_at="2025-08-06T08:41:39", category_id=1),
    )

    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Attention Is All You Need",
        "author": "Ashish Vaswani et al.",
        "isbn": "9780123456786",
        "price": 22000,
        "stock_quantity": 5,
        "published_date": "2017-06-12",
        "created_at": "2025-08-06T08:24:11",
        "updated_at": "2025-08-06T08:41:39",
        "category_id": 1
    }
    # 404
    mocker.patch("api.book.get_book_by_book_id", return_value=None)

    response = client.get("/books/1")
    assert response.status_code == 404
    assert response.json() == { "detail": "Book Not Found" }

def test_create_book(client, mocker):
    create_spy = mocker.spy(Book, "create")
    mocker.patch("api.book.create_book", return_value=
        Book(id=1, title="Attention Is All You Need", author="Ashish Vaswani et al.", isbn="9780123456786", price=22000,
         stock_quantity=5, published_date="2017-06-12", created_at="2025-08-06T08:24:11",
         updated_at="2025-08-06T08:41:39", category_id=1),
    )

    body = {
        "title": "TEST",
        "author": "Juhwan Kim et al.",
        "isbn": "1234123412341",
        "price": 12345,
        "stock_quantity": 7,
        "published_date": "2000-08-24",
        "category_id": 3
    }

    response = client.post("/books", json=body)

    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.title == "TEST"
    assert create_spy.spy_return.author == "Juhwan Kim et al."
    assert create_spy.spy_return.isbn == "1234123412341"
    assert create_spy.spy_return.price == 12345
    assert create_spy.spy_return.stock_quantity == 7

    assert create_spy.spy_return.published_date == date(2000, 8, 24)
    assert create_spy.spy_return.category_id == 3

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Attention Is All You Need",
        "author": "Ashish Vaswani et al.",
        "isbn": "9780123456786",
        "price": 22000,
        "stock_quantity": 5,
        "published_date": "2017-06-12",
        "created_at": "2025-08-06T08:24:11",
        "updated_at": "2025-08-06T08:41:39",
        "category_id": 1
    }

def test_update_book(client, mocker):
    # 200

    mock_original = Book(
        id=1, title="Attention Is All You Need", author="Ashish Vaswani et al.", isbn="9780123456786", price=22000,
        stock_quantity=5, published_date="2017-06-12", created_at="2025-08-06T08:24:11",
        updated_at="2025-08-06T08:41:39", category_id=1
    )
    mocker.patch("api.book.get_book_by_book_id", return_value=mock_original)

    # update_book의 return_value: price=100000로 바뀌어 있는지 결과만 확인하기 위해
    mock_update = mocker.patch("api.book.update_book", return_value=
    Book(id=1, title="Attention Is All You Need", author="Ashish Vaswani et al.", isbn="9780123456786", price=100000,
         stock_quantity=5, published_date="2017-06-12", created_at="2025-08-06T08:24:11",
         updated_at="2025-08-06T08:41:39", category_id=1)
    )

    response = client.patch("/books/1", json={"price": 1234567})

    # 여기서 mock_update 함수 argument 검증, assert_called_once_with는 pytest-mock에 정의된 메소드
    mock_update.assert_called_once_with(
        session=ANY,
        book=mock_original,
        request=UpdateBookRequest(price=1234567)
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Attention Is All You Need",
        "author": "Ashish Vaswani et al.",
        "isbn": "9780123456786",
        "price": 100000,
        "stock_quantity": 5,
        "published_date": "2017-06-12",
        "created_at": "2025-08-06T08:24:11",
        "updated_at": "2025-08-06T08:41:39",
        "category_id": 1
    }
    # 404
    mocker.patch("api.book.get_book_by_book_id", return_value=None)

    response = client.patch("/books/1", json={"price": 100000})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book Not Found"}

def test_delete_book(client, mocker):
    # 204
    mocker.patch("api.book.get_book_by_book_id", return_value=
    Book(id=1, title="Attention Is All You Need", author="Ashish Vaswani et al.", isbn="9780123456786", price=22000,
         stock_quantity=5, published_date="2017-06-12", created_at="2025-08-06T08:24:11",
         updated_at="2025-08-06T08:41:39", category_id=1),
    )
    mocker.patch("api.book.delete_book", return_value=None)

    response = client.delete("/books/1")
    assert response.status_code == 204
    # 404
    mocker.patch("api.book.get_book_by_book_id", return_value=None)

    response = client.delete("/books/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book Not Found"}