"""
Category API 테스트
- CRUD 기능 테스트
- 유효성 검증 테스트
- 에러 케이스 테스트
"""
import os
import sys
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, Mock

# Add week05 assignment path to sys.path for imports
week05_example_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "week05_assignment", "example"))
if week05_example_path not in sys.path:
    sys.path.insert(0, week05_example_path)

from models.category import Category


class TestCategoryAPI:
    """카테고리 API 테스트 클래스"""
    
    def test_create_category_success(self, test_client: TestClient):
        """
        카테고리 생성 성공 테스트
        - 정상적인 데이터로 카테고리 생성
        - 201 상태 코드 확인
        - 응답 데이터 검증
        """
        # Arrange
        category_data = {
            "name": "테스트 카테고리",
            "description": "테스트용 카테고리입니다"
        }
        
        # Act
        response = test_client.post("/api/v1/categories", json=category_data)
        
        # Assert
        assert response.status_code == 201
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["message"] == "카테고리가 성공적으로 생성되었습니다"
        
        category_response = response_data["data"]
        assert category_response["name"] == category_data["name"]
        assert category_response["description"] == category_data["description"]
        assert category_response["id"] is not None
        assert category_response["book_count"] == 0
    
    def test_create_category_duplicate_name(self, test_client: TestClient, sample_category: Category):
        """
        중복된 카테고리명으로 생성 실패 테스트
        - 이미 존재하는 카테고리명으로 생성 시도
        - 400 상태 코드 확인
        - 적절한 에러 메시지 확인
        """
        # Arrange
        category_data = {
            "name": sample_category.name,  # 이미 존재하는 카테고리명
            "description": "중복 테스트"
        }
        
        # Act
        response = test_client.post("/api/v1/categories", json=category_data)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
        assert "이미 존재" in response_data["message"]
    
    def test_create_category_invalid_data(self, test_client: TestClient):
        """
        잘못된 데이터로 카테고리 생성 실패 테스트
        - 필수 필드 누락
        - 400 상태 코드 확인
        """
        # Arrange - 필수 필드(name) 누락
        category_data = {
            "description": "이름이 없는 카테고리"
        }
        
        # Act
        response = test_client.post("/api/v1/categories", json=category_data)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
    
    def test_create_category_empty_name(self, test_client: TestClient):
        """
        빈 이름으로 카테고리 생성 실패 테스트
        """
        # Arrange
        category_data = {
            "name": "",
            "description": "빈 이름 테스트"
        }
        
        # Act
        response = test_client.post("/api/v1/categories", json=category_data)
        
        # Assert
        assert response.status_code == 400
    
    def test_get_all_categories_empty(self, test_client: TestClient):
        """
        빈 카테고리 목록 조회 테스트
        - 카테고리가 없을 때 빈 리스트 반환
        - 200 상태 코드 확인
        """
        # Arrange - 데이터 없음
        
        # Act
        response = test_client.get("/api/v1/categories")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert response_data["data"] == []
        assert "0개의 카테고리" in response_data["message"]
    
    def test_get_all_categories_with_data(self, test_client: TestClient, sample_categories: list[Category]):
        """
        카테고리 목록 조회 테스트 (데이터 있음)
        - 등록된 카테고리들 조회
        - 정확한 개수 확인
        - 데이터 구조 검증
        """
        # Arrange - sample_categories 픽스처로 데이터 준비됨
        
        # Act
        response = test_client.get("/api/v1/categories")
        
        # Assert
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert len(response_data["data"]) == len(sample_categories)
        assert f"{len(sample_categories)}개의 카테고리" in response_data["message"]
        
        # 첫 번째 카테고리 데이터 검증
        first_category = response_data["data"][0]
        assert "id" in first_category
        assert "name" in first_category
        assert "description" in first_category
        assert "book_count" in first_category
        assert "created_at" in first_category
        assert "updated_at" in first_category
    
    def test_get_all_categories_performance(self, test_client: TestClient, large_dataset):
        """
        대용량 데이터에서 카테고리 조회 성능 테스트
        - 응답 시간 체크
        - 메모리 사용량 체크
        """
        # Arrange - large_dataset 픽스처로 대용량 데이터 준비
        
        # Act
        import time
        start_time = time.time()
        response = test_client.get("/api/v1/categories")
        end_time = time.time()
        
        # Assert
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # 1초 이내 응답
        
        response_data = response.json()
        assert response_data["status"] == "success"
        assert len(response_data["data"]) > 0


class TestCategoryAPIErrorHandling:
    """카테고리 API 에러 처리 테스트"""
    
    def test_create_category_database_error(self, test_client: TestClient):
        """
        데이터베이스 오류 시 처리 테스트
        - 데이터베이스 연결 실패 시뮬레이션
        - 500 상태 코드 확인
        """
        # Arrange
        category_data = {
            "name": "DB 오류 테스트",
            "description": "데이터베이스 오류 시뮬레이션"
        }
        
        # DB 세션 오류 모킹
        with patch('database.get_db') as mock_get_db:
            mock_db = Mock()
            mock_db.add.side_effect = Exception("Database connection failed")
            mock_get_db.return_value.__enter__.return_value = mock_db
            mock_get_db.return_value.__exit__.return_value = None
            
            # Act
            response = test_client.post("/api/v1/categories", json=category_data)
            
            # Assert
            assert response.status_code == 500
            
            response_data = response.json()
            assert response_data["status"] == "error"
            assert "서버 오류" in response_data["message"]
    
    def test_get_categories_database_error(self, test_client: TestClient):
        """
        카테고리 조회 시 데이터베이스 오류 처리 테스트
        """
        # Arrange & Act
        with patch('services.category.CategoryService.get_all_categories') as mock_service:
            mock_service.side_effect = Exception("Database query failed")
            
            response = test_client.get("/api/v1/categories")
            
            # Assert
            assert response.status_code == 500
            
            response_data = response.json()
            assert response_data["status"] == "error"
            assert "서버 오류" in response_data["message"]


class TestCategoryAPIValidation:
    """카테고리 API 유효성 검증 테스트"""
    
    @pytest.mark.parametrize("invalid_name", [
        "",  # 빈 문자열
        " ",  # 공백만
        "a" * 101,  # 100자 초과
        None,  # null 값
    ])
    def test_create_category_invalid_names(self, test_client: TestClient, invalid_name):
        """
        잘못된 카테고리명 유효성 검증 테스트
        - 다양한 잘못된 이름 패턴 테스트
        """
        # Arrange
        category_data = {
            "name": invalid_name,
            "description": "유효성 검증 테스트"
        }
        
        # Act
        response = test_client.post("/api/v1/categories", json=category_data)
        
        # Assert
        assert response.status_code == 400
        
        response_data = response.json()
        assert response_data["status"] == "error"
    
    def test_create_category_long_description(self, test_client: TestClient):
        """
        긴 설명으로 카테고리 생성 테스트
        - 설명 필드 길이 제한 확인
        """
        # Arrange
        category_data = {
            "name": "긴 설명 테스트",
            "description": "x" * 1001  # 1000자 초과
        }
        
        # Act
        response = test_client.post("/api/v1/categories", json=category_data)
        
        # Assert
        # 설명이 너무 길면 400 에러, 아니면 성공
        if response.status_code == 400:
            response_data = response.json()
            assert response_data["status"] == "error"
        else:
            assert response.status_code == 201


@pytest.mark.integration
class TestCategoryAPIIntegration:
    """카테고리 API 통합 테스트"""
    
    def test_category_workflow(self, test_client: TestClient):
        """
        카테고리 전체 워크플로우 테스트
        - 생성 → 조회 → 확인 순서
        """
        # Arrange
        categories_to_create = [
            {"name": "프로그래밍", "description": "프로그래밍 서적"},
            {"name": "디자인", "description": "디자인 관련 서적"},
            {"name": "경영", "description": "경영 관련 서적"},
        ]
        
        created_categories = []
        
        # Act & Assert - 카테고리들 생성
        for category_data in categories_to_create:
            response = test_client.post("/api/v1/categories", json=category_data)
            assert response.status_code == 201
            created_categories.append(response.json()["data"])
        
        # Act & Assert - 전체 카테고리 조회
        response = test_client.get("/api/v1/categories")
        assert response.status_code == 200
        
        response_data = response.json()
        assert len(response_data["data"]) == len(categories_to_create)
        
        # 생성된 카테고리들이 모두 조회되는지 확인
        fetched_names = {cat["name"] for cat in response_data["data"]}
        expected_names = {cat["name"] for cat in categories_to_create}
        assert fetched_names == expected_names
    
    def test_concurrent_category_creation(self, test_client: TestClient):
        """
        동시 카테고리 생성 테스트
        - 동일한 이름으로 동시 생성 시도
        - 하나만 성공해야 함
        """
        import threading
        import time
        
        # Arrange
        category_data = {
            "name": "동시생성테스트",
            "description": "동시 생성 테스트용 카테고리"
        }
        
        results = []
        
        def create_category():
            try:
                response = test_client.post("/api/v1/categories", json=category_data)
                results.append(response.status_code)
            except Exception as e:
                results.append(str(e))
        
        # Act - 동시에 5개 스레드에서 같은 카테고리 생성 시도
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_category)
            threads.append(thread)
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Assert - 하나는 성공(201), 나머지는 실패(400)여야 함
        success_count = results.count(201)
        error_count = results.count(400)
        
        assert success_count == 1, f"Expected 1 success, got {success_count}"
        assert error_count == 4, f"Expected 4 errors, got {error_count}"