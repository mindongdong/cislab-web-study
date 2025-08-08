"""
# 📚 도서 관리 시스템 API

FastAPI와 SQLAlchemy를 활용한 RESTful API 구현

## 🚀 주요 기능

### 핵심 기능
- **도서 CRUD**: 도서 등록, 조회, 수정, 삭제
- **카테고리 관리**: 도서 분류를 위한 카테고리 시스템
- **검색 및 필터링**: 제목/저자 검색, 카테고리별/가격대별 필터링
- **페이지네이션**: 대량 데이터 처리를 위한 페이지 분할
- **재고 관리**: 실시간 재고 추가/차감 기능

### 기술적 특징
- **계층형 아키텍처**: Router → Service → Model 구조로 책임 분리
- **트랜잭션 관리**: 데이터 일관성 보장
- **N+1 문제 해결**: Eager Loading을 통한 쿼리 최적화
- **일관된 응답 형식**: 모든 API가 동일한 응답 구조 사용
- **체계적인 에러 처리**: 비즈니스 예외와 HTTP 예외 구분

## 📋 설치 및 실행

### 1. 필수 요구사항
- Python 3.8+
- MySQL 5.7+ 또는 8.0+
- pip (Python 패키지 관리자)

### 2. 프로젝트 설정

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. MySQL 데이터베이스 생성
mysql -u root -p
CREATE DATABASE book_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 4. 환경 변수 설정
# .env 파일 생성 후 데이터베이스 연결 정보 입력
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/book_management

# 5. 애플리케이션 실행
python -m app.main
# 또는
uvicorn app.main:app --reload
```

### 3. API 문서 확인
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📚 API 엔드포인트

### 카테고리 관리

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/api/v1/categories` | 카테고리 생성 |
| GET | `/api/v1/categories` | 전체 카테고리 조회 |

### 도서 관리

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/api/v1/books` | 도서 등록 |
| GET | `/api/v1/books` | 도서 목록 조회 (검색/필터/페이징) |
| GET | `/api/v1/books/{book_id}` | 도서 상세 조회 |
| PATCH | `/api/v1/books/{book_id}` | 도서 정보 수정 |
| DELETE | `/api/v1/books/{book_id}` | 도서 삭제 |
| PATCH | `/api/v1/books/{book_id}/stock` | 재고 수량 변경 |

## 📖 API 사용 예시

### 1. 카테고리 생성
```bash
curl -X POST "http://localhost:8000/api/v1/categories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "프로그래밍",
    "description": "프로그래밍 관련 도서"
  }'
```

**응답:**
```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "프로그래밍",
    "description": "프로그래밍 관련 도서",
    "created_at": "2024-08-06T10:00:00",
    "book_count": 0
  },
  "message": "카테고리가 성공적으로 생성되었습니다"
}
```

### 2. 도서 등록
```bash
curl -X POST "http://localhost:8000/api/v1/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI 완벽 가이드",
    "author": "홍길동",
    "isbn": "9781234567890",
    "price": 35000,
    "stock_quantity": 100,
    "published_date": "2024-01-15",
    "category_id": 1
  }'
```

### 3. 도서 검색 및 필터링
```bash
# 제목/저자로 검색
curl "http://localhost:8000/api/v1/books?search=FastAPI"

# 카테고리와 가격대로 필터링
curl "http://localhost:8000/api/v1/books?category_id=1&min_price=20000&max_price=50000"

# 페이지네이션
curl "http://localhost:8000/api/v1/books?page=2&size=20"
```

### 4. 재고 관리
```bash
# 재고 추가
curl -X PATCH "http://localhost:8000/api/v1/books/1/stock" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 50,
    "operation": "add"
  }'

# 재고 차감
curl -X PATCH "http://localhost:8000/api/v1/books/1/stock" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity": 10,
    "operation": "subtract"
  }'
```

## 🏗️ 프로젝트 구조

```
book_management/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── database.py              # DB 연결 설정
│   ├── models/                 # SQLAlchemy 모델
│   │   ├── book.py
│   │   └── category.py
│   ├── schemas/                # Pydantic 스키마
│   │   ├── book.py
│   │   ├── category.py
│   │   └── common.py
│   ├── routers/                # API 엔드포인트
│   │   ├── books.py
│   │   └── categories.py
│   ├── services/               # 비즈니스 로직
│   │   ├── book_service.py
│   │   └── category_service.py
│   └── utils/                  # 유틸리티
│       └── exceptions.py
├── requirements.txt
├── .env
└── README.md
```

## 🔍 주요 구현 특징

### 1. N+1 문제 해결
```python
# joinedload를 사용한 즉시 로딩
query = db.query(Book).options(joinedload(Book.category))
```

### 2. 트랜잭션과 동시성 제어
```python
# 재고 업데이트 시 행 잠금
book = db.query(Book).filter(Book.id == book_id).with_for_update().first()
```

### 3. 체계적인 예외 처리
```python
# 비즈니스 예외 계층 구조
BusinessException
├── NotFoundException
├── DuplicateException
├── InsufficientStockException
└── InvalidOperationException
```

## 🧪 테스트

```bash
# 단위 테스트 실행
pytest tests/

# 커버리지 확인
pytest --cov=app tests/
```

## 📝 추가 개발 제안

1. **인증/인가**: JWT 기반 사용자 인증
2. **캐싱**: Redis를 활용한 응답 캐싱
3. **로깅**: 구조화된 로깅 시스템
4. **API 버전관리**: 버전별 라우팅
5. **소프트 삭제**: deleted_at 필드를 활용한 논리적 삭제
6. **배치 작업**: 대량 데이터 처리 API
"""