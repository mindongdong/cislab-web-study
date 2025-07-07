# FastAPI 게시판 API 설계 과제

## 📋 과제 목표
FastAPI를 활용하여 간단한 게시판 시스템의 API를 설계하고 구현해보세요.

## 🎯 과제 체크리스트

- [ ] **경로 매개변수(Path Parameters)** 사용하기
- [ ] **쿼리 매개변수(Query Parameters)** 사용하기
- [ ] **Pydantic BaseModel** 활용하여 데이터 모델 설계하기
- [ ] 모델별 필수 필드 제외하고 3개 이상의 필드 추가로 설계하기
- [ ] **List[]** 타입 활용하기
- [ ] **Optional[]** 타입 활용하기
- [ ] **요청 본문(Request Body)** 처리하기

## 🗂️ 데이터 모델 설계

### 1. 기본 모델 구조

```python
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

# 이미 구현되어 있다고 가정하는 User 모델
class User(BaseModel):
    user_id: int
    username: str
    email: str

# 여러분이 구현해야 할 모델들
class Board(BaseModel):
    # TODO: 게시판 모델 구현
    pass

class Post(BaseModel):
    # TODO: 게시글 모델 구현
    pass

class PostCreate(BaseModel):
    # TODO: 게시글 생성용 모델 구현
    pass
```

### 2. 모델 설계 가이드라인

#### 📌 Board(게시판) 모델에 반드시 필수 필드:
- `board_id`: 게시판 고유 ID (int)
#### 📌 Post(게시글) 모델에 반드시 필수 필드:
- `post_id`: 게시글 고유 ID (int)
- `board_id`: 소속 게시판 ID (int)
- `user_id`: 작성자 ID (int)
#### 📌 PostCreate(게시글 생성) 모델에 포함해야할 필수 필드:
- `board_id`: 소속 게시판 ID (int)
- `title`: 제목 (str)

## 🛠️ 구현해야 할 API 엔드포인트

### 1. 게시판 관련 API

#### 📍 모든 게시판 목록 조회
```python
@app.get("/boards")
def get_boards():
    """모든 게시판 목록을 조회합니다."""
    # TODO: 구현
    pass
```

#### 📍 특정 게시판 조회 (경로 매개변수 사용)
```python
@app.get(?)
def get_board(
	?
):
    """특정 게시판 정보를 조회합니다."""
    # TODO: 구현
    pass
```

### 2. 게시글 관련 API
#### 📍 게시글 목록 조회 (경로 매개변수 / 쿼리 매개변수 혼합 사용)
```python
@app.get(?)
def get_posts(
    ?
):
    """특정 게시판의 게시글 목록을 조회합니다."""
    # TODO: 구현
    pass
```

#### 📍 특정 게시글 조회 (경로 매개변수 사용)
```python
@app.get(?)
def get_post(?):
    """특정 게시글을 조회합니다."""
    # TODO: 구현
    pass
```

#### 📍 게시글 생성 (요청 본문 사용)
```python
@app.post("/posts")
def create_post(
    ?
):
    """새로운 게시글을 생성합니다."""
    # TODO: 구현
    pass
```

## 🗃️ 목업 데이터 구성

### 1. 사용자 목업 데이터
```python
# 목업 사용자 데이터 (이미 구현되어 있다고 가정)
mock_users = [
    User(user_id=1, username="alice", email="alice@example.com"),
    User(user_id=2, username="bob", email="bob@example.com"),
    User(user_id=3, username="charlie", email="charlie@example.com")
]
```

### 2. 게시판 목업 데이터 (여러분이 작성)
```python
# TODO: 최소 3개 이상의 게시판 목업 데이터 작성
mock_boards = [
    # 예시: Board(board_id=1, ...)
]
```

### 3. 게시글 목업 데이터 (여러분이 작성)

```python
# TODO: 최소 3개 이상의 게시글 목업 데이터 작성
mock_posts = [
    # 예시: Post(post_id=1, board_id=1, user_id=1, title="첫 번째 게시글", ...)
]
```

## 🔧 구현 단계별 가이드

### Step 0: 프로젝트 설정
1. .gitignore, requirements.txt 파일 lectures/lecture01 폴더에서 복사해서 사용하세요
2. 프로젝트 폴더 구조는 아래와 같이 설정하세요
```
week01_assignment/
├── .gitignore
├── requirements.txt
├── main.py
```

### Step 1: 데이터 모델 정의
1. `Board`, `Post`, `PostCreate` 모델을 완성하세요
2. 각 필드에 적절한 타입 힌트를 작성하세요
3. Optional 필드와 List 필드를 적절히 활용하세요

### Step 2: 목업 데이터 작성
1. 게시판 목업 데이터 3개 이상 작성
2. 게시글 목업 데이터 5개 이상 작성 (다양한 게시판에 분산)
3. 현실적인 예시 데이터 사용 (실제 게시판처럼)

### Step 3: API 엔드포인트 구현
1. 각 엔드포인트에서 적절한 목업 데이터를 반환하도록 구현
2. 경로 매개변수와 쿼리 매개변수를 활용한 필터링 로직 구현
3. 에러 처리 (존재하지 않는 ID 등)

### Step 4: 테스트 및 문서화
1. `uvicorn main:app --reload`로 서버 실행
2. `http://localhost:8000/docs`에서 자동 생성된 API 문서 확인
3. 각 엔드포인트 테스트

## 📝 제출 요구사항

### 1. 코드 파일 (`main.py`)
- 완성된 FastAPI 애플리케이션 코드
- 모든 모델 정의 및 API 엔드포인트 구현
- 목업 데이터 포함

### 2. 코드 설명 파일 (`README.md`)
- 코드 설명 및 실행 방법 포함
- 코드 설명 파일은 코드 파일과 동일한 폴더에 위치해야 합니다.

## 🚀 완성 후 확인사항
1. **자동 문서화**: `/docs` 페이지에서 모든 API가 올바르게 문서화되는지 확인
2. **타입 검증**: 잘못된 타입 입력 시 적절한 에러 메시지 반환 확인
3. **기능 테스트**: 각 엔드포인트가 예상대로 동작하는지 확인
