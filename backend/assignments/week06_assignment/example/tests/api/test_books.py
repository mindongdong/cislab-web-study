"""
Book API 테스트
- CRUD 기능 테스트
- 검색 및 필터링 테스트
- 페이지네이션 테스트
- 재고 관리 테스트
- 에러 케이스 테스트
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, Mock
from datetime import date

# Add week05 assignment path to sys.path for imports
week05_example_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "week05_assignment", "example"))
if week05_example_path not in sys.path:
    sys.path.insert(0, week05_example_path)

from models.book import Book
from models.category import Category


class TestBookAPI:
    """도서 API 기본 CRUD 테스트"""
    
    def test_create_book_success(self, test_client: TestClient, sample_category: Category):
        """
        도서 생성 성공 테스트
        - 정상적인 데이터로 도서 생성
        - 201 상태 코드 확인
        - 응답 데이터 검증
        """
        # Arrange
        book_data = {
            "title": "테스트 도서",
            "author": "테스트 저자",
            "isbn": "9788901234567",
            "price": 25000,
            "stock_quantity": 10,
            "published_date": "2023-01-01",
            "category_id": sample_category.id
        }
        
        # Act
        response = test_client.post("/api/v1/books", json=book_data)
        
        # Assert
        assert response.status_code == 201
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "도서가 성공적으로 등록되었습니다"
        
        book_response = response_data["data"]
        assert book_response["title"] == book_data["title"]
        assert book_response["author"] == book_data["author"]
        assert book_response["isbn"] == book_data["isbn"]
        assert book_response["price"] == book_data["price"]
        assert book_response["stock_quantity"] == book_data["stock_quantity"]
        assert book_response["category"]["id"] == sample_category.id
    
    def test_create_book_duplicate_isbn(self, test_client: TestClient, sample_book: Book):
        """
        중복 ISBN으로 도서 생성 실패 테스트
        """
        # Arrange
        book_data = {
            "title": "다른 제목",
            "author": "다른 저자",
            "isbn": sample_book.isbn,  # 중복 ISBN
            "price": 30000,
            "stock_quantity": 5,
            "category_id": sample_book.category_id
        }
        
        # Act
        response = test_client.post("/api/v1/books", json=book_data)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "ISBN" in response_data["message"]
    
    def test_create_book_invalid_category(self, test_client: TestClient):
        """
        존재하지 않는 카테고리로 도서 생성 실패 테스트
        """
        # Arrange
        book_data = {
            "title": "테스트 도서",
            "author": "테스트 저자",
            "isbn": "9788901234567",
            "price": 25000,
            "stock_quantity": 10,
            "category_id": 99999  # 존재하지 않는 카테고리 ID
        }
        
        # Act
        response = test_client.post("/api/v1/books", json=book_data)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "카테고리" in response_data["message"]
    
    @pytest.mark.parametrize("invalid_isbn", [
        "123",  # 너무 짧음
        "12345678901234",  # 너무 김
        "abcd1234567890",  # 숫자가 아닌 문자 포함
        "",  # 빈 문자열
    ])
    def test_create_book_invalid_isbn(self, test_client: TestClient, sample_category: Category, invalid_isbn):
        """
        잘못된 ISBN으로 도서 생성 실패 테스트
        """
        # Arrange
        book_data = {
            "title": "테스트 도서",
            "author": "테스트 저자",
            "isbn": invalid_isbn,
            "price": 25000,
            "stock_quantity": 10,
            "category_id": sample_category.id
        }
        
        # Act
        response = test_client.post("/api/v1/books", json=book_data)
        
        # Assert
        assert response.status_code == 400
    
    def test_get_book_by_id_success(self, test_client: TestClient, sample_book: Book):
        """
        도서 ID로 조회 성공 테스트
        """
        # Arrange - sample_book 픽스처로 데이터 준비
        
        # Act
        response = test_client.get(f"/api/v1/books/{sample_book.id}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        
        book_data = response_data["data"]
        assert book_data["id"] == sample_book.id
        assert book_data["title"] == sample_book.title
        assert book_data["author"] == sample_book.author
        assert book_data["isbn"] == sample_book.isbn
        assert book_data["category"]["id"] == sample_book.category_id
    
    def test_get_book_by_id_not_found(self, test_client: TestClient):
        """
        존재하지 않는 도서 ID로 조회 실패 테스트
        """
        # Arrange
        non_existent_id = 99999
        
        # Act
        response = test_client.get(f"/api/v1/books/{non_existent_id}")
        
        # Assert
        assert response.status_code == 404
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "찾을 수 없습니다" in response_data["message"]
    
    def test_update_book_success(self, test_client: TestClient, sample_book: Book):
        """
        도서 정보 수정 성공 테스트
        """
        # Arrange
        update_data = {
            "title": "수정된 제목",
            "price": 40000
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{sample_book.id}", json=update_data)
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "도서 정보가 성공적으로 수정되었습니다"
        
        book_data = response_data["data"]
        assert book_data["title"] == update_data["title"]
        assert book_data["price"] == update_data["price"]
        # 수정되지 않은 필드는 그대로 유지
        assert book_data["author"] == sample_book.author
        assert book_data["isbn"] == sample_book.isbn
    
    def test_update_book_not_found(self, test_client: TestClient):
        """
        존재하지 않는 도서 수정 실패 테스트
        """
        # Arrange
        non_existent_id = 99999
        update_data = {"title": "수정된 제목"}
        
        # Act
        response = test_client.patch(f"/api/v1/books/{non_existent_id}", json=update_data)
        
        # Assert
        assert response.status_code == 404
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "찾을 수 없습니다" in response_data["message"]
    
    def test_delete_book_success(self, test_client: TestClient, sample_book: Book):
        """
        도서 삭제 성공 테스트
        """
        # Arrange
        book_id = sample_book.id
        
        # Act
        response = test_client.delete(f"/api/v1/books/{book_id}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "도서가 성공적으로 삭제되었습니다"
        
        # 삭제 후 조회 시 404 확인
        get_response = test_client.get(f"/api/v1/books/{book_id}")
        assert get_response.status_code == 404
    
    def test_delete_book_not_found(self, test_client: TestClient):
        """
        존재하지 않는 도서 삭제 실패 테스트
        """
        # Arrange
        non_existent_id = 99999
        
        # Act
        response = test_client.delete(f"/api/v1/books/{non_existent_id}")
        
        # Assert
        assert response.status_code == 404
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "찾을 수 없습니다" in response_data["message"]


class TestBookSearchAndFilter:
    """도서 검색 및 필터링 테스트"""
    
    def test_get_books_all(self, test_client: TestClient, sample_books: list[Book]):
        """
        전체 도서 조회 테스트
        """
        # Arrange - sample_books 픽스처로 데이터 준비
        
        # Act
        response = test_client.get("/api/v1/books")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert len(response_data["data"]) == len(sample_books)
        
        # 페이지네이션 메타 정보 확인
        meta = response_data["meta"]
        assert meta["page"] == 1
        assert meta["size"] == 10
        assert meta["total"] == len(sample_books)
    
    def test_search_books_by_title(self, test_client: TestClient, sample_books: list[Book]):
        """
        제목으로 도서 검색 테스트
        """
        # Arrange
        search_term = "Clean"  # sample_books 중 "Clean Code" 검색
        
        # Act
        response = test_client.get(f"/api/v1/books?search={search_term}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        
        # 검색 결과 확인
        books = response_data["data"]
        assert len(books) > 0
        
        # 모든 검색 결과에 검색어가 포함되어 있는지 확인
        for book in books:
            assert search_term.lower() in book["title"].lower()
    
    def test_search_books_by_author(self, test_client: TestClient, sample_books: list[Book]):
        """
        저자로 도서 검색 테스트
        """
        # Arrange
        search_term = "Martin"  # "Robert C. Martin" 검색
        
        # Act
        response = test_client.get(f"/api/v1/books?search={search_term}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        
        books = response_data["data"]
        assert len(books) > 0
        
        for book in books:
            assert search_term.lower() in book["author"].lower()
    
    def test_filter_books_by_category(self, test_client: TestClient, sample_books: list[Book], sample_categories: list[Category]):
        """
        카테고리별 도서 필터링 테스트
        """
        # Arrange
        category_id = sample_categories[0].id
        
        # Act
        response = test_client.get(f"/api/v1/books?category_id={category_id}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        books = response_data["data"]
        
        # 모든 결과가 해당 카테고리에 속하는지 확인
        for book in books:
            assert book["category"]["id"] == category_id
    
    def test_filter_books_by_price_range(self, test_client: TestClient, sample_books: list[Book]):
        """
        가격대별 도서 필터링 테스트
        """
        # Arrange
        min_price = 30000
        max_price = 50000
        
        # Act
        response = test_client.get(f"/api/v1/books?min_price={min_price}&max_price={max_price}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        books = response_data["data"]
        
        # 모든 결과가 가격 범위 안에 있는지 확인
        for book in books:
            assert min_price <= book["price"] <= max_price
    
    def test_complex_search_filter(self, test_client: TestClient, sample_books: list[Book], sample_categories: list[Category]):
        """
        복합 검색 및 필터링 테스트
        """
        # Arrange
        search_term = "Python"
        category_id = sample_categories[0].id
        min_price = 20000
        
        # Act
        response = test_client.get(
            f"/api/v1/books?search={search_term}&category_id={category_id}&min_price={min_price}"
        )
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        books = response_data["data"]
        
        # 복합 조건 확인
        for book in books:
            # 검색어 포함 확인 (제목 또는 저자)
            has_search_term = (
                search_term.lower() in book["title"].lower() or 
                search_term.lower() in book["author"].lower()
            )
            assert has_search_term
            # 카테고리 확인
            assert book["category"]["id"] == category_id
            # 최소 가격 확인
            assert book["price"] >= min_price
    
    def test_search_no_results(self, test_client: TestClient):
        """
        검색 결과 없음 테스트
        """
        # Arrange
        search_term = "존재하지않는도서"
        
        # Act
        response = test_client.get(f"/api/v1/books?search={search_term}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert len(response_data["data"]) == 0
        assert response_data["meta"]["total"] == 0


class TestBookPagination:
    """도서 페이지네이션 테스트"""
    
    def test_pagination_first_page(self, test_client: TestClient, large_dataset):
        """
        첫 번째 페이지 조회 테스트
        """
        # Arrange
        page = 1
        size = 10
        
        # Act
        response = test_client.get(f"/api/v1/books?page={page}&size={size}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data["data"]) == size
        
        meta = response_data["meta"]
        assert meta["page"] == page
        assert meta["size"] == size
        assert meta["total"] == 100  # large_dataset은 100개 데이터
        assert meta["total_pages"] == 10
    
    def test_pagination_middle_page(self, test_client: TestClient, large_dataset):
        """
        중간 페이지 조회 테스트
        """
        # Arrange
        page = 5
        size = 10
        
        # Act
        response = test_client.get(f"/api/v1/books?page={page}&size={size}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data["data"]) == size
        
        meta = response_data["meta"]
        assert meta["page"] == page
        assert meta["size"] == size
    
    def test_pagination_last_page(self, test_client: TestClient, large_dataset):
        """
        마지막 페이지 조회 테스트
        """
        # Arrange
        page = 10
        size = 10
        
        # Act
        response = test_client.get(f"/api/v1/books?page={page}&size={size}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data["data"]) == size
        
        meta = response_data["meta"]
        assert meta["page"] == page
        assert meta["total_pages"] == page
    
    def test_pagination_out_of_range(self, test_client: TestClient, large_dataset):
        """
        범위를 벗어난 페이지 조회 테스트
        """
        # Arrange
        page = 999
        size = 10
        
        # Act
        response = test_client.get(f"/api/v1/books?page={page}&size={size}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data["data"]) == 0  # 빈 결과
        
        meta = response_data["meta"]
        assert meta["page"] == page
        assert meta["total"] == 100
    
    @pytest.mark.parametrize("size", [1, 5, 20, 50, 100])
    def test_pagination_different_sizes(self, test_client: TestClient, large_dataset, size):
        """
        다양한 페이지 크기 테스트
        """
        # Arrange
        page = 1
        
        # Act
        response = test_client.get(f"/api/v1/books?page={page}&size={size}")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        expected_count = min(size, 100)  # 전체 데이터가 100개이므로
        assert len(response_data["data"]) == expected_count
        
        meta = response_data["meta"]
        assert meta["size"] == size
    
    def test_pagination_invalid_parameters(self, test_client: TestClient):
        """
        잘못된 페이지네이션 파라미터 테스트
        """
        # Arrange & Act & Assert
        # 음수 페이지
        response = test_client.get("/api/v1/books?page=-1")
        assert response.status_code == 400
        
        # 0 페이지
        response = test_client.get("/api/v1/books?page=0")
        assert response.status_code == 400
        
        # 음수 크기
        response = test_client.get("/api/v1/books?size=-1")
        assert response.status_code == 400
        
        # 너무 큰 크기 (101개 초과)
        response = test_client.get("/api/v1/books?size=101")
        assert response.status_code == 400


class TestBookStockManagement:
    """도서 재고 관리 테스트"""
    
    def test_update_stock_add(self, test_client: TestClient, sample_book: Book):
        """
        재고 추가 테스트
        """
        # Arrange
        initial_stock = sample_book.stock_quantity
        add_quantity = 5
        stock_update = {
            "quantity": add_quantity,
            "operation": "add"
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{sample_book.id}/stock", json=stock_update)
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert "추가" in response_data["message"]
        
        book_data = response_data["data"]
        assert book_data["stock_quantity"] == initial_stock + add_quantity
    
    def test_update_stock_subtract(self, test_client: TestClient, sample_book: Book):
        """
        재고 차감 테스트
        """
        # Arrange
        initial_stock = sample_book.stock_quantity
        subtract_quantity = 3
        stock_update = {
            "quantity": subtract_quantity,
            "operation": "subtract"
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{sample_book.id}/stock", json=stock_update)
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert "차감" in response_data["message"]
        
        book_data = response_data["data"]
        assert book_data["stock_quantity"] == initial_stock - subtract_quantity
    
    def test_update_stock_insufficient(self, test_client: TestClient, sample_book: Book):
        """
        재고 부족 시 차감 실패 테스트
        """
        # Arrange
        excessive_quantity = sample_book.stock_quantity + 1
        stock_update = {
            "quantity": excessive_quantity,
            "operation": "subtract"
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{sample_book.id}/stock", json=stock_update)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "재고" in response_data["message"]
    
    def test_update_stock_invalid_operation(self, test_client: TestClient, sample_book: Book):
        """
        잘못된 재고 연산 테스트
        """
        # Arrange
        stock_update = {
            "quantity": 5,
            "operation": "invalid_operation"
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{sample_book.id}/stock", json=stock_update)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
    
    def test_update_stock_negative_quantity(self, test_client: TestClient, sample_book: Book):
        """
        음수 수량으로 재고 업데이트 실패 테스트
        """
        # Arrange
        stock_update = {
            "quantity": -5,
            "operation": "add"
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{sample_book.id}/stock", json=stock_update)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
    
    def test_update_stock_book_not_found(self, test_client: TestClient):
        """
        존재하지 않는 도서의 재고 업데이트 실패 테스트
        """
        # Arrange
        non_existent_id = 99999
        stock_update = {
            "quantity": 5,
            "operation": "add"
        }
        
        # Act
        response = test_client.patch(f"/api/v1/books/{non_existent_id}/stock", json=stock_update)
        
        # Assert
        assert response.status_code == 404
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "찾을 수 없습니다" in response_data["message"]


@pytest.mark.integration
class TestBookAPIIntegration:
    """도서 API 통합 테스트"""
    
    def test_book_lifecycle(self, test_client: TestClient, sample_category: Category):
        """
        도서 전체 생명주기 테스트
        - 생성 → 조회 → 수정 → 재고 관리 → 삭제
        """
        # Arrange
        book_data = {
            "title": "통합 테스트 도서",
            "author": "통합 테스트 저자",
            "isbn": "9788901234567",
            "price": 25000,
            "stock_quantity": 10,
            "published_date": "2023-01-01",
            "category_id": sample_category.id
        }
        
        # Act & Assert - 1. 도서 생성
        create_response = test_client.post("/api/v1/books", json=book_data)
        assert create_response.status_code == 201
        
        book_id = create_response.json()["data"]["id"]
        
        # Act & Assert - 2. 도서 조회
        get_response = test_client.get(f"/api/v1/books/{book_id}")
        assert get_response.status_code == 200
        
        book = get_response.json()["data"]
        assert book["title"] == book_data["title"]
        
        # Act & Assert - 3. 도서 수정
        update_data = {"title": "수정된 제목", "price": 30000}
        update_response = test_client.patch(f"/api/v1/books/{book_id}", json=update_data)
        assert update_response.status_code == 200
        
        updated_book = update_response.json()["data"]
        assert updated_book["title"] == update_data["title"]
        assert updated_book["price"] == update_data["price"]
        
        # Act & Assert - 4. 재고 관리
        stock_update = {"quantity": 5, "operation": "add"}
        stock_response = test_client.patch(f"/api/v1/books/{book_id}/stock", json=stock_update)
        assert stock_response.status_code == 200
        
        stock_book = stock_response.json()["data"]
        assert stock_book["stock_quantity"] == book_data["stock_quantity"] + 5
        
        # Act & Assert - 5. 도서 삭제
        delete_response = test_client.delete(f"/api/v1/books/{book_id}")
        assert delete_response.status_code == 200
        
        # 삭제 확인
        final_get_response = test_client.get(f"/api/v1/books/{book_id}")
        assert final_get_response.status_code == 404
    
    def test_search_pagination_integration(self, test_client: TestClient, large_dataset):
        """
        검색과 페이지네이션 통합 테스트
        """
        # Arrange
        search_term = "Test"  # large_dataset의 모든 도서 제목에 포함
        page_size = 20
        
        # Act - 첫 번째 페이지
        response1 = test_client.get(f"/api/v1/books?search={search_term}&page=1&size={page_size}")
        assert response1.status_code == 200
        
        data1 = response1.json()
        assert len(data1["data"]) == page_size
        assert data1["meta"]["page"] == 1
        
        # Act - 두 번째 페이지
        response2 = test_client.get(f"/api/v1/books?search={search_term}&page=2&size={page_size}")
        assert response2.status_code == 200
        
        data2 = response2.json()
        assert len(data2["data"]) == page_size
        assert data2["meta"]["page"] == 2
        
        # Assert - 페이지 간 중복 없음
        page1_ids = {book["id"] for book in data1["data"]}
        page2_ids = {book["id"] for book in data2["data"]}
        assert page1_ids.isdisjoint(page2_ids)