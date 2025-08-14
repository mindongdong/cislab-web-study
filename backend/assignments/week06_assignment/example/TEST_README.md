# 도서 관리 시스템 API 테스트 가이드

이 문서는 FastAPI 기반 도서 관리 시스템의 포괄적인 테스트 스위트에 대한 실행 가이드입니다.

## 📋 목차

1. [테스트 환경 설정](#테스트-환경-설정)
2. [테스트 실행 방법](#테스트-실행-방법)
3. [테스트 구조](#테스트-구조)
4. [테스트 커버리지](#테스트-커버리지)
5. [CI/CD 통합](#cicd-통합)
6. [문제 해결](#문제-해결)

## 🛠️ 테스트 환경 설정

### 1. 의존성 설치

먼저 테스트에 필요한 의존성을 설치합니다:

```bash
# 기본 의존성 설치
pip install -r requirements.txt

# 테스트 의존성 설치
pip install -r requirements-test.txt
```

### 2. 환경 변수 설정

테스트 실행을 위한 환경 변수를 설정합니다:

```bash
# .env.test 파일 생성
export TESTING=1
export DATABASE_URL="sqlite:///:memory:"
export LOG_LEVEL="INFO"
```

### 3. 테스트 데이터베이스

- 테스트는 **In-Memory SQLite 데이터베이스**를 사용합니다
- 각 테스트는 독립적인 트랜잭션에서 실행되어 격리를 보장합니다
- 테스트 종료 후 자동으로 데이터가 정리됩니다

## 🚀 테스트 실행 방법

### 기본 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 상세한 출력과 함께 실행
pytest -v

# 실패한 테스트만 재실행
pytest --lf

# 특정 마커의 테스트만 실행
pytest -m "unit"
pytest -m "integration"
pytest -m "api"
```

### 테스트 커버리지와 함께 실행

```bash
# 커버리지와 함께 실행 (HTML 리포트 생성)
pytest --cov=. --cov-report=html

# 터미널에서 커버리지 확인
pytest --cov=. --cov-report=term-missing

# 커버리지 최소 기준 확인 (80%)
pytest --cov=. --cov-fail-under=80
```

### 병렬 테스트 실행

```bash
# 4개 프로세스로 병렬 실행
pytest -n 4

# 자동으로 CPU 코어 수만큼 병렬 실행
pytest -n auto
```

### 특정 테스트 파일/클래스/함수 실행

```bash
# 특정 파일의 모든 테스트 실행
pytest tests/api/test_books.py

# 특정 클래스의 테스트 실행
pytest tests/api/test_books.py::TestBookAPI

# 특정 테스트 함수 실행
pytest tests/api/test_books.py::TestBookAPI::test_create_book_success

# 패턴으로 테스트 선택
pytest -k "book and create"
```

### 디버깅 모드

```bash
# 첫 번째 실패에서 중단
pytest -x

# pdb 디버거 자동 시작
pytest --pdb

# 출력 캡처 비활성화 (print 문 출력 보기)
pytest -s
```

## 📁 테스트 구조

### 디렉토리 구조

```
tests/
├── __init__.py                 # 테스트 패키지 초기화
├── conftest.py                 # 공통 픽스처 및 설정
├── pytest.ini                 # pytest 설정
├── api/                        # API 엔드포인트 테스트
│   ├── __init__.py
│   ├── test_books.py          # 도서 API 테스트
│   └── test_categories.py     # 카테고리 API 테스트
├── test_main.py               # 메인 애플리케이션 테스트
└── test_mocking.py            # 모킹 및 외부 서비스 테스트
```

### 테스트 카테고리

#### 1. API 테스트 (`tests/api/`)

- **도서 API 테스트** (`test_books.py`):
  - CRUD 기능 (생성, 조회, 수정, 삭제)
  - 검색 및 필터링
  - 페이지네이션
  - 재고 관리
  - 에러 케이스

- **카테고리 API 테스트** (`test_categories.py`):
  - 카테고리 생성/조회
  - 중복 검증
  - 유효성 검사
  - 에러 처리

#### 2. 애플리케이션 테스트 (`test_main.py`)

- 루트 엔드포인트
- 헬스체크
- 미들웨어 (CORS)
- 예외 처리기
- API 문서 접근성

#### 3. 모킹 테스트 (`test_mocking.py`)

- 외부 서비스 모킹 (ISBN 검증, 이메일)
- 데이터베이스 오류 시뮬레이션
- 캐싱 서비스 테스트
- Circuit Breaker 패턴

### 픽스처 (Fixtures)

#### 데이터베이스 픽스처

```python
@pytest.fixture(scope="session")
def test_db_engine():
    """세션 스코프 DB 엔진"""

@pytest.fixture(scope="function") 
def db_session():
    """함수 스코프 DB 세션 (테스트 격리)"""

@pytest.fixture(scope="function")
def test_client():
    """FastAPI 테스트 클라이언트"""
```

#### 데이터 픽스처

```python
@pytest.fixture
def sample_category():
    """단일 카테고리"""

@pytest.fixture
def sample_categories():
    """다중 카테고리"""

@pytest.fixture
def sample_book():
    """단일 도서"""

@pytest.fixture
def sample_books():
    """다중 도서"""

@pytest.fixture
def large_dataset():
    """성능 테스트용 대용량 데이터"""
```

#### 모킹 픽스처

```python
@pytest.fixture
def mock_external_service():
    """외부 서비스 모킹"""

@pytest.fixture
def mock_email_service():
    """이메일 서비스 모킹"""

@pytest.fixture
def mock_isbn_validator():
    """ISBN 검증 서비스 모킹"""
```

## 📊 테스트 커버리지

### 커버리지 목표

- **전체 커버리지**: 80% 이상
- **단위 테스트**: 90% 이상
- **통합 테스트**: 70% 이상

### 커버리지 리포트 확인

```bash
# HTML 리포트 생성 후 브라우저에서 확인
pytest --cov=. --cov-report=html
open htmlcov/index.html

# 터미널에서 누락된 라인 확인
pytest --cov=. --cov-report=term-missing
```

### 커버리지 제외 설정

`.coveragerc` 파일로 제외할 파일/라인 설정:

```ini
[run]
omit = 
    tests/*
    venv/*
    */migrations/*
    manage.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 🔄 CI/CD 통합

### GitHub Actions 예시

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        pytest --cov=. --cov-report=xml --cov-fail-under=80
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### 로컬 Git Hooks

```bash
# pre-commit hook 설정
pip install pre-commit
pre-commit install

# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

## 🛠️ 문제 해결

### 일반적인 문제들

#### 1. 테스트 데이터베이스 연결 문제

```bash
# 해결책: 환경 변수 확인
export DATABASE_URL="sqlite:///:memory:"
export TESTING=1
```

#### 2. 픽스처 의존성 오류

```python
# 올바른 픽스처 순서 확인
def test_example(db_session, sample_category, sample_book):
    # sample_book은 sample_category에 의존
```

#### 3. 모킹이 작동하지 않음

```python
# 정확한 모듈 경로 사용
@patch('services.book.BookService.get_all_books')  # 올바른 경로
# @patch('app.services.book_service.BookService.get_all_books')  # 잘못된 경로
```

#### 4. 병렬 테스트 실행 시 오류

```bash
# 데이터베이스 경합 조건 방지
pytest -n auto --dist=loadfile
```

### 성능 최적화

#### 1. 테스트 실행 속도 향상

```python
# 트랜잭션 롤백 사용 (빠른 클린업)
@pytest.fixture(scope="function")
def db_session():
    transaction = connection.begin()
    yield session
    transaction.rollback()

# 대용량 데이터 지연 로딩
@pytest.fixture
def large_dataset():
    return create_large_dataset_lazy()
```

#### 2. 메모리 사용량 최적화

```python
# 픽스처 스코프 최적화
@pytest.fixture(scope="session")  # 세션 전체에서 재사용
def expensive_resource():
    return create_expensive_resource()
```

### 테스트 작성 가이드라인

#### AAA 패턴 (Arrange-Act-Assert)

```python
def test_create_book_success(self, test_client, sample_category):
    # Arrange (준비)
    book_data = {
        "title": "테스트 도서",
        "author": "테스트 저자",
        # ... 나머지 데이터
    }
    
    # Act (실행)
    response = test_client.post("/api/v1/books", json=book_data)
    
    # Assert (검증)
    assert response.status_code == 201
    assert response.json()["status"] == "success"
```

#### 테스트 명명 규칙

```python
# 패턴: test_{기능}_{시나리오}_{예상결과}
def test_create_book_success(self):
    """정상적인 도서 생성 성공 테스트"""

def test_create_book_duplicate_isbn_failure(self):
    """중복 ISBN으로 도서 생성 실패 테스트"""
```

#### 파라미터화된 테스트

```python
@pytest.mark.parametrize("invalid_isbn", [
    "123",           # 너무 짧음
    "12345678901234", # 너무 김
    "abcd1234567890", # 잘못된 형식
])
def test_create_book_invalid_isbn(self, test_client, invalid_isbn):
    """다양한 잘못된 ISBN 형식 테스트"""
```

## 📋 테스트 실행 체크리스트

### 개발 단계

- [ ] 새 기능 구현 시 단위 테스트 작성
- [ ] API 엔드포인트 추가 시 통합 테스트 작성
- [ ] 에러 케이스 테스트 포함
- [ ] 모킹이 필요한 외부 의존성 확인

### PR 생성 전

- [ ] 모든 테스트 통과 확인: `pytest`
- [ ] 커버리지 80% 이상 확인: `pytest --cov=. --cov-fail-under=80`
- [ ] 새로운 코드에 대한 테스트 추가
- [ ] 테스트 실행 시간 확인 (5분 이내)

### 배포 전

- [ ] 전체 테스트 스위트 실행
- [ ] 성능 테스트 확인
- [ ] 통합 테스트 통과 확인
- [ ] 프로덕션 유사 환경에서 테스트

---

## 📞 지원

테스트 관련 문제가 있을 경우:

1. **로그 확인**: `pytest -v -s` 로 자세한 출력 확인
2. **픽스처 디버깅**: `--setup-show` 옵션으로 픽스처 실행 순서 확인
3. **개별 테스트 실행**: 문제가 있는 특정 테스트만 실행
4. **문서 참조**: [pytest 공식 문서](https://docs.pytest.org/)

테스트 코드는 애플리케이션 코드만큼 중요합니다. 신뢰할 수 있는 테스트 스위트로 안정적인 개발을 이어가세요! 🚀