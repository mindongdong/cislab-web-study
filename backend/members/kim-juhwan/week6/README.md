## FastAPI 테스트 코드 실습 과제: 도서 관리 시스템 API 테스트

### 📌 과제 개요

5회차에서 구현한 도서 관리 시스템 API에 대한 테스트 코드를 작성하세요. **인프런 강의 섹션 4. 테스트 코드**에서 학습한 PyTest를 활용하여 단위 테스트와 통합 테스트를 구현해봅니다.

### 📋 요구사항

#### 1. 테스트 환경 설정

- PyTest 설치 및 설정 ✅
- 테스트용 데이터베이스 분리 (SQLite 또는 테스트용 MySQL) ❌
- conftest.py 파일 작성 ✅
- 테스트 디렉토리 구조 설정 ✅

#### 2. Fixture 구현 (필수) ⚠️

다음 Fixture들을 구현하세요:

```python
# 예시
@pytest.fixture
def test_client():
    """테스트용 FastAPI 클라이언트"""
    pass

@pytest.fixture
def test_db():
    """테스트용 데이터베이스 세션"""
    pass

@pytest.fixture
def sample_category():
    """테스트용 카테고리 데이터"""
    pass

@pytest.fixture
def sample_book():
    """테스트용 도서 데이터"""
    pass
```

#### 3. API 엔드포인트 테스트 구현

**Book API 테스트 (필수)** 각 테스트는 최소 2개 이상의 시나리오를 포함해야 합니다.

1. **GET /books 테스트**
    
    - 정상 조회 (빈 목록, 데이터 있는 경우) ✅
    - 페이지네이션 동작 확인 ✅
    - 필터링 기능 테스트 (category_id, price range) ✅
    - 검색 기능 테스트 ✅
2. **GET /books/{book_id} 테스트**
    
    - 정상 조회 ✅
    - 존재하지 않는 ID 조회 (404 에러) ✅
    - 잘못된 ID 형식 (400 에러) ✅
3. **POST /books 테스트**
    
    - 정상 생성 ✅
    - 필수 필드 누락
    - 유효하지 않은 데이터 (ISBN 형식, 음수 가격 등)
    - 중복 ISBN 
4. **PATCH /books/{book_id} 테스트**
    
    - 정상 수정 ✅
    - 일부 필드만 수정 ✅
    - 존재하지 않는 도서 수정 시도
    - 유효하지 않은 데이터
5. **DELETE /books/{book_id} 테스트**
    
    - 정상 삭제 ✅
    - 존재하지 않는 도서 삭제 시도
    - 삭제 후 재조회 확인
6. **PATCH /books/{book_id}/stock 테스트**
    
    - 재고 추가
    - 재고 차감
    - 재고 부족 시 차감 시도
    - 잘못된 operation 값

**Category API 테스트 (필수)**

1. **POST /categories 테스트**
    
    - 정상 생성
    - 중복 이름으로 생성 시도
2. **GET /categories 테스트**
    
    - 전체 목록 조회

#### 4. Mocking 활용 (필수)

최소 2개 이상의 Mocking 테스트를 구현하세요:

- 외부 서비스 호출 모킹 (예: ISBN 검증 API)
- 데이터베이스 에러 상황 모킹
- 현재 시간 모킹 (created_at, updated_at 테스트)

#### 5. 테스트 커버리지 ✅

- pytest-cov를 사용하여 테스트 커버리지 측정
- 최소 80% 이상의 코드 커버리지 달성
- 커버리지 리포트 생성
