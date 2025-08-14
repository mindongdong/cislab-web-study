"""
Main 애플리케이션 테스트
- 루트 엔드포인트 테스트
- 헬스체크 테스트
- 미들웨어 테스트
- 예외 처리 테스트
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Add week05 assignment path to sys.path for imports
week05_example_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "week05_assignment", "example"))
if week05_example_path not in sys.path:
    sys.path.insert(0, week05_example_path)


class TestMainApplication:
    """메인 애플리케이션 테스트"""
    
    def test_root_endpoint(self, test_client: TestClient):
        """
        루트 엔드포인트 테스트
        - API 상태 확인
        - 기본 정보 반환 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act
        response = test_client.get("/")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "도서 관리 시스템 API가 정상적으로 실행 중입니다"
        
        data = response_data["data"]
        assert data["version"] == "1.0.0"
        assert data["docs"] == "/docs"
        assert data["redoc"] == "/redoc"
    
    def test_health_check_endpoint(self, test_client: TestClient):
        """
        헬스체크 엔드포인트 테스트
        - 서비스 상태 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act
        response = test_client.get("/health")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "서비스가 정상 작동 중입니다"
        assert response_data["data"]["status"] == "healthy"
    
    def test_docs_endpoint_accessible(self, test_client: TestClient):
        """
        API 문서 엔드포인트 접근 테스트
        - Swagger UI 접근 가능성 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act
        response = test_client.get("/docs")
        
        # Assert
        assert response.status_code == 200
        # Swagger UI HTML이 반환되는지 확인
        assert "swagger" in response.text.lower() or "openapi" in response.text.lower()
    
    def test_redoc_endpoint_accessible(self, test_client: TestClient):
        """
        ReDoc 엔드포인트 접근 테스트
        - ReDoc 문서 접근 가능성 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act
        response = test_client.get("/redoc")
        
        # Assert
        assert response.status_code == 200
        # ReDoc HTML이 반환되는지 확인
        assert "redoc" in response.text.lower() or "openapi" in response.text.lower()
    
    def test_openapi_json_accessible(self, test_client: TestClient):
        """
        OpenAPI JSON 스키마 접근 테스트
        - API 스키마 정보 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act
        response = test_client.get("/openapi.json")
        
        # Assert
        assert response.status_code == 200
        
        openapi_data = response.json()
        assert openapi_data["info"]["title"] == "도서 관리 시스템 API"
        assert openapi_data["info"]["version"] == "1.0.0"
        assert "paths" in openapi_data
        assert "/api/v1/books" in openapi_data["paths"]
        assert "/api/v1/categories" in openapi_data["paths"]


class TestMiddleware:
    """미들웨어 테스트"""
    
    def test_cors_middleware(self, test_client: TestClient):
        """
        CORS 미들웨어 테스트
        - CORS 헤더 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act - OPTIONS 요청 (preflight)
        response = test_client.options("/api/v1/books")
        
        # Assert
        assert response.status_code == 200
        
        # CORS 헤더 확인
        headers = response.headers
        assert "access-control-allow-origin" in headers
        assert "access-control-allow-methods" in headers
        assert "access-control-allow-headers" in headers
    
    def test_cors_actual_request(self, test_client: TestClient):
        """
        실제 CORS 요청 테스트
        - 실제 API 요청 시 CORS 헤더 포함 확인
        """
        # Arrange
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
        
        # Act
        response = test_client.get("/api/v1/books", headers=headers)
        
        # Assert
        assert response.status_code == 200
        
        # CORS 헤더가 응답에 포함되어 있는지 확인
        assert "access-control-allow-origin" in response.headers


class TestExceptionHandlers:
    """예외 처리기 테스트"""
    
    def test_business_exception_handler(self, test_client: TestClient):
        """
        비즈니스 예외 처리기 테스트
        - 중복 ISBN으로 도서 생성 시 비즈니스 예외 발생
        """
        # Arrange - 먼저 도서 하나 생성
        book_data = {
            "title": "테스트 도서",
            "author": "테스트 저자",
            "isbn": "9788901234567",
            "price": 25000,
            "stock_quantity": 10
        }
        
        first_response = test_client.post("/api/v1/books", json=book_data)
        assert first_response.status_code == 201
        
        # Act - 같은 ISBN으로 두 번째 도서 생성 시도
        response = test_client.post("/api/v1/books", json=book_data)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert response_data["data"] is None
        assert "ISBN" in response_data["message"]
    
    def test_validation_exception_handler(self, test_client: TestClient):
        """
        유효성 검증 예외 처리기 테스트
        - 잘못된 데이터 형식으로 요청 시 검증 오류
        """
        # Arrange - 잘못된 데이터 (price가 문자열)
        invalid_book_data = {
            "title": "테스트 도서",
            "author": "테스트 저자",
            "isbn": "9788901234567",
            "price": "잘못된가격",  # 숫자가 아닌 문자열
            "stock_quantity": 10
        }
        
        # Act
        response = test_client.post("/api/v1/books", json=invalid_book_data)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert response_data["message"] == "입력 데이터가 유효하지 않습니다"
        assert "data" in response_data
        assert "details" in response_data["data"]
    
    def test_http_exception_handler(self, test_client: TestClient):
        """
        HTTP 예외 처리기 테스트
        - 존재하지 않는 엔드포인트 접근 시 404 처리
        """
        # Arrange - 존재하지 않는 엔드포인트
        
        # Act
        response = test_client.get("/api/v1/nonexistent")
        
        # Assert
        assert response.status_code == 404
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert response_data["data"] is None
    
    def test_general_exception_handler(self, test_client: TestClient):
        """
        일반 예외 처리기 테스트
        - 예상치 못한 서버 오류 시 500 응답
        """
        # Arrange & Act - 서버 오류 발생 시뮬레이션을 위해 모킹 사용
        with patch('services.book.BookService.get_all_books') as mock_service:
            mock_service.side_effect = Exception("Unexpected server error")
            
            response = test_client.get("/api/v1/books")
        
        # Assert
        assert response.status_code == 500
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert response_data["message"] == "서버 내부 오류가 발생했습니다"
        assert response_data["data"] is None


class TestAPIRouting:
    """API 라우팅 테스트"""
    
    def test_api_prefix_routing(self, test_client: TestClient):
        """
        API 프리픽스 라우팅 테스트
        - /api/v1 프리픽스가 정상 작동하는지 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act & Assert - Books API
        books_response = test_client.get("/api/v1/books")
        assert books_response.status_code == 200
        
        # Act & Assert - Categories API
        categories_response = test_client.get("/api/v1/categories")
        assert categories_response.status_code == 200
    
    def test_invalid_api_prefix(self, test_client: TestClient):
        """
        잘못된 API 프리픽스 테스트
        - /api/v2 등 존재하지 않는 버전으로 접근 시 404
        """
        # Arrange - 잘못된 API 버전
        
        # Act
        response = test_client.get("/api/v2/books")
        
        # Assert
        assert response.status_code == 404
    
    def test_missing_api_prefix(self, test_client: TestClient):
        """
        API 프리픽스 누락 테스트
        - /books (프리픽스 없음) 접근 시 404
        """
        # Arrange - 프리픽스 없는 경로
        
        # Act
        response = test_client.get("/books")
        
        # Assert
        assert response.status_code == 404


class TestResponseFormat:
    """응답 형식 테스트"""
    
    def test_success_response_format(self, test_client: TestClient):
        """
        성공 응답 형식 테스트
        - 모든 성공 응답이 일관된 형식을 가지는지 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act
        response = test_client.get("/api/v1/categories")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        # 필수 필드 확인
        assert "status" in response_data
        assert "data" in response_data
        assert "message" in response_data
        
        # 성공 응답 값 확인
        assert response_data["status"] == "success"
        assert isinstance(response_data["data"], list)
        assert isinstance(response_data["message"], str)
    
    def test_error_response_format(self, test_client: TestClient):
        """
        오류 응답 형식 테스트
        - 모든 오류 응답이 일관된 형식을 가지는지 확인
        """
        # Arrange - 존재하지 않는 도서 ID
        
        # Act
        response = test_client.get("/api/v1/books/99999")
        
        # Assert
        assert response.status_code == 404
        
        response_data = response.json()
        # 필수 필드 확인
        assert "status" in response_data
        assert "message" in response_data
        
        # 오류 응답 값 확인
        assert response_data["status"] == "error"
        assert isinstance(response_data["message"], str)
    
    def test_paginated_response_format(self, test_client: TestClient, large_dataset):
        """
        페이지네이션 응답 형식 테스트
        - 페이지네이션이 적용된 응답의 메타 정보 확인
        """
        # Arrange - large_dataset으로 데이터 준비
        
        # Act
        response = test_client.get("/api/v1/books?page=1&size=10")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        # 기본 응답 필드
        assert "status" in response_data
        assert "data" in response_data
        assert "message" in response_data
        
        # 페이지네이션 메타 필드
        assert "meta" in response_data
        
        meta = response_data["meta"]
        assert "page" in meta
        assert "size" in meta
        assert "total" in meta
        assert "total_pages" in meta
        
        # 메타 데이터 유효성 확인
        assert meta["page"] == 1
        assert meta["size"] == 10
        assert meta["total"] >= 0
        assert meta["total_pages"] >= 0


@pytest.mark.integration
class TestApplicationIntegration:
    """애플리케이션 통합 테스트"""
    
    def test_full_application_workflow(self, test_client: TestClient):
        """
        전체 애플리케이션 워크플로우 테스트
        - 루트 접근 → 헬스체크 → API 사용 → 문서 확인
        """
        # Arrange - 준비 과정 없음
        
        # Act & Assert - 1. 루트 엔드포인트 확인
        root_response = test_client.get("/")
        assert root_response.status_code == 200
        assert root_response.json()["status"] == "success"
        
        # Act & Assert - 2. 헬스체크 확인
        health_response = test_client.get("/health")
        assert health_response.status_code == 200
        assert health_response.json()["data"]["status"] == "healthy"
        
        # Act & Assert - 3. API 기능 확인
        books_response = test_client.get("/api/v1/books")
        assert books_response.status_code == 200
        
        categories_response = test_client.get("/api/v1/categories")
        assert categories_response.status_code == 200
        
        # Act & Assert - 4. API 문서 접근 확인
        docs_response = test_client.get("/docs")
        assert docs_response.status_code == 200
        
        openapi_response = test_client.get("/openapi.json")
        assert openapi_response.status_code == 200
    
    def test_concurrent_requests(self, test_client: TestClient):
        """
        동시 요청 처리 테스트
        - 여러 요청이 동시에 처리되는지 확인
        """
        import threading
        import time
        
        # Arrange
        results = []
        
        def make_request():
            start_time = time.time()
            response = test_client.get("/api/v1/books")
            end_time = time.time()
            results.append({
                "status_code": response.status_code,
                "response_time": end_time - start_time
            })
        
        # Act - 동시에 10개 요청 발송
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        end_time = time.time()
        
        # Assert
        assert len(results) == 10
        
        # 모든 요청이 성공했는지 확인
        for result in results:
            assert result["status_code"] == 200
        
        # 동시 요청 처리가 순차 처리보다 빠른지 확인
        total_time = end_time - start_time
        sequential_time = sum(result["response_time"] for result in results)
        assert total_time < sequential_time  # 동시 처리가 더 빠름