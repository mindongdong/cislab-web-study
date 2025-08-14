import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import datetime

from app.main import app
from app.db.base import Base
from app.api.deps import get_db

TEST_DB_URL = "sqlite:///./test.db" # URL

@pytest.fixture(scope="session", autouse=True) # 세션
def _prepare_db():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    Base.metadata.drop_all(bind=engine) # 초기화
    Base.metadata.create_all(bind=engine) # 생성
    yield
    engine.dispose() # 종료
    for p in ["./test.db", "./test.db-wal", "./test.db-shm", "./test.db-journal"]:
        if os.path.exists(p):
            try:
                os.remove(p) # 산출물 삭제
            except OSError:
                pass

@pytest.fixture # db세션
def db_session():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}) # SQLAlchemy
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    try:
        yield session # db 세션
        session.rollback() # 종료시 롤백
    finally:
        session.close() # 종료

@pytest.fixture # 클라이언트
def client(db_session):
    def override_get_db():
        try:
            yield db_session # 세션 주입
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db # 의존성 오버라이드
    with TestClient(app) as c: # 동기 테스트 클라이언트
        yield c
    app.dependency_overrides.clear() # 오버라이드 해제

def _mk_cat(client, name="General"): # category 생성
    return client.post("/categories", json={"name": name}).json()["data"]["id"] # id만 반환

# category
def test_create_category_ok(client):
    r = client.post("/categories", json={"name": "SF", "description": "Sci-Fi"}) # 생성
    assert r.status_code == 200 # 200 확인
    body = r.json()
    assert body["status"] == "success" # 성공 상태
    assert body["data"]["name"] == "SF" # 필드 검증

def test_create_category_duplicate(client):
    client.post("/categories", json={"name": "History"}) # 생성
    r = client.post("/categories", json={"name": "History"}) # 중복 생성
    assert r.status_code in (400, 409) # 중복 처리 확인

# book
def test_list_books_empty(client):
    r = client.get("/books") # 목록 조회
    assert r.status_code == 200 # 200 확인
    assert r.json()["data"] == [] # 빈 목록

def test_create_book_ok(client):
    cat_id = _mk_cat(client, "Fiction")
    payload = {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "1234567890123",
        "price": 12000,
        "stock_quantity": 5,
        "category_id": cat_id,
    }
    r = client.post("/books", json=payload) # 생성
    assert r.status_code == 200 # 200 확인
    data = r.json()["data"]
    assert data["isbn"] == "1234567890123" # ISBN 검증
    assert data["category"]["id"] == cat_id # 카테고리 검증

def test_get_book_detail(client):
    cat_id = _mk_cat(client, "Essay")
    book = client.post("/books", json={
        "title": "Test Book",
        "author": "Someone",
        "isbn": "1111111111111",
        "price": 1000,
        "stock_quantity": 1,
        "category_id": cat_id,
    }).json()["data"] # 선행 생성
    r = client.get(f"/books/{book['id']}") # 상세 조회
    assert r.status_code == 200 # 200 확인
    assert r.json()["data"]["title"] == "Test Book" # 필드 검증

def test_search_filter_pagination(client):
    cat_a = _mk_cat(client, "A"); cat_b = _mk_cat(client, "B") # 두 카테고리
    for b in [
        {"title":"Alpha","author":"AA","isbn":"2000000000000","price":1000,"stock_quantity":1,"category_id":cat_a},
        {"title":"Beta","author":"BB","isbn":"2000000000001","price":2000,"stock_quantity":1,"category_id":cat_a},
        {"title":"Gamma","author":"CC","isbn":"2000000000002","price":3000,"stock_quantity":1,"category_id":cat_b},
    ]:
        client.post("/books", json=b) # 더미 데이터 삽입

    r = client.get("/books", params={"search":"Al"}) # 검색
    assert any(it["title"]=="Alpha" for it in r.json()["data"]) # 검색 검증

    r = client.get("/books", params={"category_id":cat_b}) # 카테고리 필터
    assert all(it["category"]["id"]==cat_b for it in r.json()["data"]) # 필터 검증

    r = client.get("/books", params={"min_price":1500,"max_price":2500}) # 가격 필터
    assert {it["title"] for it in r.json()["data"]} == {"Beta"} # 범위 검증

    r = client.get("/books", params={"page":1,"size":2}) # 페이지네이션
    assert len(r.json()["data"]) == 2 # 페이지 크기 검증

def test_update_and_delete_book(client):
    cat_id = _mk_cat(client, "C")
    b = client.post("/books", json={
        "title":"ToUpdate","author":"Auth","isbn":"2222222222222",
        "price":5000,"stock_quantity":2,"category_id":cat_id
    }).json()["data"] # 선행 생성

    r = client.patch(f"/books/{b['id']}", json={"price":7000}) # 부분 수정
    assert r.status_code == 200 and r.json()["data"]["price"] == 7000 # 수정 검증

    r = client.patch(f"/books/{b['id']}/stock", json={"quantity":3,"operation":"add"}) # 재고 추가
    assert r.status_code == 200 and r.json()["data"]["stock_quantity"] == 5 # 재고 검증

    r = client.delete(f"/books/{b['id']}") # 삭제
    assert r.status_code == 200 # 200 확인
    assert client.get(f"/books/{b['id']}").status_code == 404 # 삭제 확인

# mocking
def test_updated_at_mock(client):
    fixed = datetime(2030,1,1,0,0,0) # 고정 시간
    with patch("app.api.routes.books.datetime") as dt: # datetime 모킹
        dt.utcnow.return_value = fixed # utcnow 고정
        b = client.post("/books", json={
            "title":"MockTime","author":"A","isbn":"3333333333333","price":1,"stock_quantity":0
        }).json()["data"] # 선행 생성
        r = client.patch(f"/books/{b['id']}", json={"price":2}) # 업데이트
        assert r.status_code == 200 # 200 확인
        assert r.json()["data"]["updated_at"].startswith("2030-01-01") # 시간 검증

def test_db_error_mock_on_category(client, db_session):
    orig = db_session.commit # 원본 백업
    def boom():
        raise IntegrityError(None, None, Exception("UNIQUE constraint failed: categories.name")) # 무결성 예외
    db_session.commit = boom # 커밋 모킹
    try:
        r = client.post("/categories", json={"name":"Dup"}) # 커밋 시 에러 유발
        assert r.status_code in (400, 409) # 에러 처리 검증
    finally:
        db_session.commit = orig # 복구
