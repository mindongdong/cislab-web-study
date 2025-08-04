## FastAPI + SQLAlchemy 실습 과제: 도서 관리 시스템 API 구축

### 📌 과제 개요

간단한 도서 관리 시스템의 RESTful API를 구현하세요. **인프런 강의 섹션 3. 데이터베이스**에서 학습한 SQLAlchemy ORM과 FastAPI를 활용하여 CRUD 기능을 구현해봅니다.

### 📋 요구사항

#### 1. 데이터베이스 모델링

다음 두 개의 테이블을 설계하고 ORM 모델을 작성하세요:

**Book 테이블**

- id (Primary Key, Auto Increment)
- title (문자열, 필수, 최대 200자)
- author (문자열, 필수, 최대 100자)
- isbn (문자열, 고유값, 13자리)
- price (정수, 필수)
- stock_quantity (정수, 기본값 0)
- published_date (날짜)
- created_at (타임스탬프, 자동 생성)
- updated_at (타임스탬프, 자동 업데이트)

**Category 테이블**

- id (Primary Key, Auto Increment)
- name (문자열, 필수, 고유값, 최대 50자)
- description (텍스트, 선택)
- created_at (타임스탬프, 자동 생성)

**관계 설정**

- Book과 Category는 다대일 관계 (한 책은 하나의 카테고리에 속함)

#### 2. API 엔드포인트 구현

**기본 CRUD (필수)**

- `POST /books` - 새 도서 등록
    
- `GET /books` - 전체 도서 목록 조회
    
- `GET /books/{book_id}` - 특정 도서 상세 조회
    
- `PATCH /books/{book_id}` - 도서 정보 수정
    
- `DELETE /books/{book_id}` - 도서 삭제
    
- `POST /categories` - 카테고리 생성
    
- `GET /categories` - 전체 카테고리 목록 조회
    

**추가 기능 (필수)**

1. **검색 기능**: `GET /books?search={keyword}`
    
    - 제목 또는 저자명에 keyword가 포함된 도서 검색
2. **필터링**: `GET /books?category_id={id}&min_price={price}&max_price={price}`
    
    - 카테고리별, 가격대별 필터링
3. **페이지네이션**: `GET /books?page={page}&size={size}`
    
    - 기본값: page=1, size=10
4. **재고 관리**: `PATCH /books/{book_id}/stock`
    
    - Request Body: `{"quantity": 5, "operation": "add" | "subtract"}`
    - 재고 추가/차감 기능

#### 3. 추가 요구사항

**응답 형식**

- 모든 응답은 다음 형식을 따라야 합니다:

```python
{
    "status": "success" | "error",
    "data": {...} | [...],  # 실제 데이터
    "message": "설명 메시지",
    "meta": {  # 페이지네이션 시에만
        "page": 1,
        "size": 10,
        "total": 100
    }
}
```

**유효성 검증**

- Pydantic을 사용한 요청/응답 스키마 정의
- ISBN은 13자리 숫자 검증
- 가격은 0 이상의 정수
- 재고는 0 이상의 정수 (차감 시 음수 불가)

**에러 처리**

- 존재하지 않는 리소스 접근 시 404 에러
- 유효하지 않은 데이터 입력 시 400 에러
- 적절한 에러 메시지 반환

### 평가 기준

1. **데이터베이스 모델링** (15점)
    
    - 테이블 스키마 설계의 적절성
    - ORM 모델 클래스 구현
    - 관계 설정 및 제약조건 구현
    - 타임스탬프 자동 처리
2. **API 엔드포인트 구현** (20점)
    
    - 모든 필수 CRUD 엔드포인트 구현
    - RESTful API 설계 원칙 준수
    - 적절한 HTTP 메서드와 상태 코드 사용
    - 일관된 응답 형식 구현
3. **SQLAlchemy ORM 활용** (15점)
    
    - 효율적인 쿼리 작성
    - 관계 데이터 조회 최적화 (N+1 문제 해결)
    - 트랜잭션 처리
    - 필터링, 정렬, 페이지네이션 구현
4. **유효성 검증 및 에러 처리** (15점)
    
    - Pydantic 스키마를 활용한 데이터 검증
    - 적절한 에러 메시지와 상태 코드 반환
    - 예외 상황 처리 (404, 400, 500 등)
    - 비즈니스 로직 검증 (재고 음수 방지 등)
5. **코드 구조 및 품질** (15점)
    
    - 계층별 책임 분리 (라우터, 서비스, 모델)
    - 코드 재사용성과 모듈화
    - 명확한 함수/변수 네이밍
    - 타입 힌트 사용
6. **추가 기능 구현** (10점)
    
    - 검색 기능의 정확성
    - 필터링 조건 조합 처리
    - 재고 관리 기능의 안정성
    - 페이지네이션 메타 정보 제공
7. **문서화** (10점)
    
    - README.md의 완성도
    - API 문서의 명확성
    - 설치 및 실행 가이드
    - 예제 요청/응답 제공

### 💡 힌트

- SQLAlchemy의 `filter()`, `like()`, `and_()`, `or_()` 등을 활용하세요
- 페이지네이션은 `offset()`과 `limit()`을 사용합니다
- 관계 데이터를 조회할 때는 `joinedload()` 또는 `selectinload()`를 고려하세요
- 트랜잭션 처리를 위해 `db.commit()`과 `db.rollback()`을 적절히 사용하세요
### 📁 제출 방법

1. 프로젝트 전체가 아닌 핵심 코드가 들어있는 파일들만 [your-position]/members/[your-name]/week5 폴더에 업로드
2. README.md 파일에 다음 내용 포함:
    - 프로젝트 설정 방법
    - API 문서 (엔드포인트, 요청/응답 예시)
### ⏰ 제출 기한

- 8월 8일 금요일까지