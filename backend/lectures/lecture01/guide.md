# FastAPI 실습 환경 설정 및 실행 가이드

## 📋 목차
1. [환경 설정](#환경-설정)
2. [서버 실행](#서버-실행)
3. [API 테스트 방법](#api-테스트-방법)
4. [모듈별 기능 가이드](#모듈별-기능-가이드)
5. [문제 해결](#문제-해결)

---

## 🔧 환경 설정

### 1. Python 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
# venv\Scripts\activate
```

### 2. 의존성 설치

```bash
# requirements.txt를 사용하여 패키지 설치
pip install -r requirements.txt

# 또는 개별 설치
pip install fastapi uvicorn[standard] pydantic email-validator python-multipart
```

### 3. 설치 확인

```bash
# 설치된 패키지 확인
pip list

# FastAPI 버전 확인
python -c "import fastapi; print(fastapi.__version__)"
```

---

## 🚀 서버 실행

### 개발 서버 실행 (권장)

```bash
# 기본 실행 (자동 재시작 활성화)
uvicorn main:app --reload

# 포트 지정 실행
uvicorn main:app --reload --port 8000

# 호스트 및 포트 지정
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 상세 로그와 함께 실행
uvicorn main:app --reload --log-level debug
```

### 성공적인 실행 확인

서버가 성공적으로 실행되면 다음과 같은 메시지가 출력됩니다:

```
INFO:     Will watch for changes in these directories: ['/path/to/lecture01']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🧪 API 테스트 방법

### 1. 웹 브라우저에서 확인

```bash
# API 홈페이지
http://localhost:8000

# Swagger UI (자동 생성된 API 문서)
http://localhost:8000/docs

# ReDoc (대안 API 문서)
http://localhost:8000/redoc
```

### 2. HTML 클라이언트 사용

```bash
# 프로젝트에 포함된 테스트 클라이언트 열기
open client.html

# 또는 웹 브라우저에서 직접 열기
# file:///Users/dongminshin/Documents/GitHub/cislab-web-study/backend/lectures/lecture01/client.html
```

### 3. curl 명령어로 테스트

```bash
# 기본 API 테스트
curl http://localhost:8000

# 경로 매개변수 테스트
curl http://localhost:8000/path/items/42

# 쿼리 매개변수 테스트
curl "http://localhost:8000/query/search?q=FastAPI&page=1&limit=5"

# POST 요청 테스트 (사용자 생성)
curl -X POST "http://localhost:8000/body/users" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "홍길동",
    "email": "hong@example.com",
    "password": "Password123!",
    "age": 30,
    "terms_accepted": true
  }'
```

---

## 📚 모듈별 기능 가이드

### 1. 경로 매개변수 (Path Parameters) - `modules/path_parameters.py`

**학습 내용**: URL 경로에 포함된 변수 처리

**주요 엔드포인트**:
```bash
# 기본 상품 조회
GET /path/items/{item_id}
예시: http://localhost:8000/path/items/42

# 모델 정보 조회 (Enum 사용)
GET /path/models/{model_name}
예시: http://localhost:8000/path/models/resnet

# 파일 경로 처리
GET /path/files/{file_path:path}
예시: http://localhost:8000/path/files/documents/report.pdf
```

**실습 포인트**:
- 숫자 범위 검증 (1-1000)
- Enum을 사용한 제한된 선택지
- 경로 매개변수 타입 변환

### 2. 쿼리 매개변수 (Query Parameters) - `modules/query_parameters.py`

**학습 내용**: URL 쿼리 스트링 처리 및 필터링

**주요 엔드포인트**:
```bash
# 검색 API
GET /query/search?q=검색어&page=1&limit=10&sort=asc

# 상품 필터링
GET /query/items?skip=0&limit=10&category=electronics&min_price=50&in_stock=true

# 사용자 목록 (boolean 매개변수)
GET /query/users?active=true&role=admin&page=1&size=20

# 리포트 생성 (필수 매개변수)
GET /query/reports?start_date=2024-01-01&end_date=2024-01-31&report_type=monthly

# 상품 조회 (리스트 매개변수)
GET /query/products?tags=electronics&tags=sale&categories=laptop&ids=1&ids=2
```

**실습 포인트**:
- 선택적/필수 매개변수
- 타입 자동 변환 (bool, int, float)
- 리스트 매개변수 처리
- 정규식 검증

### 3. 요청 본문 (Request Body) - `modules/request_body.py`

**학습 내용**: JSON 데이터 처리 및 Pydantic 모델 검증

**주요 엔드포인트**:
```bash
# 사용자 생성
POST /body/users
Content-Type: application/json
{
  "name": "홍길동",
  "email": "hong@example.com",
  "password": "Password123!",
  "age": 30,
  "terms_accepted": true
}

# 사용자 정보 수정
PUT /body/users/{user_id}
{
  "name": "김철수",
  "age": 25
}

# 작업 생성 (Body() 추가 매개변수)
POST /body/users/{user_id}/tasks
{
  "task": {
    "title": "API 문서 작성",
    "priority": "medium",
    "due_date": "2024-02-01"
  },
  "notify": true
}

# 상품 생성 (고급 검증)
POST /body/products
{
  "name": "고급 노트북",
  "price": 1299999,
  "category": "electronics",
  "sku": "LAP123456",
  "weight": 2.5,
  "tags": ["노트북", "고성능"]
}
```

**실습 포인트**:
- Pydantic 모델 검증
- 커스텀 validator 사용
- 다중 본문 매개변수
- Field를 사용한 상세 검증

### 4. 중첩 모델 (Nested Models) - `modules/nested_models.py`

**학습 내용**: 복잡한 데이터 구조 처리

**주요 엔드포인트**:
```bash
# 상품 생성 (중첩 모델)
POST /nested/items
{
  "name": "노트북",
  "price": 1299.99,
  "tags": ["gaming", "laptop"],
  "images": [
    {
      "url": "https://picsum.photos/800/600",
      "name": "메인 이미지",
      "type": "jpeg",
      "size": 1024000
    }
  ],
  "category": {
    "id": 1,
    "name": "컴퓨터"
  }
}

# 제안 생성 (깊게 중첩된 구조)
POST /nested/offers
{
  "name": "게이밍 세트",
  "items": [...],
  "seller": {
    "name": "게이밍샵",
    "company": {
      "name": "(주)게이밍코리아",
      "address": {
        "street": "서울특별시 강남구",
        "city": "서울",
        "country": "KR"
      }
    }
  }
}

# 예시 데이터 확인
GET /nested/examples
```

**실습 포인트**:
- 깊게 중첩된 모델 구조
- List, Set, Dict 타입 사용
- HttpUrl, 정규식 검증
- 자동 계산 필드

### 5. 숫자 검증 (Numeric Validation) - `modules/numeric_validation.py`

**학습 내용**: 고급 숫자 검증 및 제약 조건

**주요 엔드포인트**:
```bash
# 기본 숫자 검증
GET /validation/items/{item_id}?rating=4.5

# 검색 (복합 숫자 검증)
GET /validation/search?q=test&page=1&size=10&min_price=50&max_price=500

# 고급 필터링
GET /validation/advanced-filter?price_min=100&price_max=1000&stock_min=10&rating_exact=4.5

# 범위 통계
GET /validation/range-stats?min_value=0&max_value=100&sample_size=50
```

**실습 포인트**:
- ge, gt, le, lt 검증 키워드
- Path, Query 메타데이터
- 키워드 인자 강제 (*)
- 복합 검증 로직

---

## 🔍 API 탐색 가이드

### Swagger UI 사용법

1. **브라우저에서 접속**: `http://localhost:8000/docs`
2. **모듈별 섹션 확인**: 각 모듈이 별도 태그로 분류됨
3. **Try it out 버튼**: 실제 API 호출 테스트
4. **Response 확인**: 응답 데이터와 HTTP 상태 코드 확인

### 클라이언트 HTML 사용법

1. **파일 열기**: `client.html`을 더블클릭하여 브라우저에서 열기
2. **섹션별 테스트**: 각 API 모듈별로 구분된 테스트 섹션
3. **실시간 테스트**: 입력값 변경 후 즉시 테스트 가능
4. **종합 테스트**: 모든 API를 한 번에 테스트하는 기능

---

## ⚠️ 문제 해결

### 일반적인 문제

**1. 모듈을 찾을 수 없음 오류**
```bash
ModuleNotFoundError: No module named 'fastapi'
```
**해결책**: 가상환경이 활성화되었는지 확인하고 requirements.txt 재설치

**2. 포트가 이미 사용 중**
```bash
ERROR: [Errno 48] Address already in use
```
**해결책**: 다른 포트 사용 `uvicorn main:app --reload --port 8001`

**3. CORS 오류 (브라우저에서 클라이언트 사용 시)**
```bash
Access to fetch at 'http://localhost:8000' from origin 'null' has been blocked by CORS policy
```
**해결책**: 이미 main.py에 CORS 설정이 포함되어 있음. 브라우저 새로고침 시도

### 디버깅 팁

**1. 상세 로그 확인**
```bash
uvicorn main:app --reload --log-level debug
```

**2. 수동 API 테스트**
```bash
# 서버 상태 확인
curl http://localhost:8000

# 응답 헤더 포함하여 확인
curl -i http://localhost:8000
```

**3. Python 인터프리터에서 확인**
```python
import fastapi
import uvicorn
print(f"FastAPI 버전: {fastapi.__version__}")
print(f"Uvicorn 버전: {uvicorn.__version__}")
```

---

## 🎯 학습 순서 권장

1. **환경 설정 완료** → 서버 실행 확인
2. **Path Parameters** → 기본 URL 처리 학습
3. **Query Parameters** → 검색 및 필터링 학습
4. **Request Body** → JSON 데이터 처리 학습
5. **Nested Models** → 복잡한 구조 처리 학습
6. **Numeric Validation** → 고급 검증 학습

각 모듈을 학습할 때는:
- Swagger UI에서 API 스키마 확인
- client.html에서 실제 테스트
- 코드에서 구현 세부사항 확인

---

## 🔗 추가 리소스

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 문서](https://docs.pydantic.dev/)
- [Uvicorn 문서](https://www.uvicorn.org/)

---

**Happy Coding! 🚀**