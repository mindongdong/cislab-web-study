# tests/conftest.py
import os, sys, pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from layer.main import app
from layer.connection import get_db
from layer.orm import Base, Book, Category

#mysql에 테스트 전용 database 하나 만듦.
engine = create_engine(
    "mysql+pymysql://root:1234@127.0.0.1:3306/book_test",
)
TestSessionFactory = sessionmaker(bind=engine)

# 테이블 생성 1회. 기존의 테이블을 삭제하고 다시 생성
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

#테스트용 db생성
@pytest.fixture
def test_db():
    session = TestSessionFactory()
    try:
        session.query(Book).delete()
        session.query(Category).delete()
        session.commit()
        yield session
    finally:
        session.close()

#테스트용 get_db생성
@pytest.fixture(autouse=True) #테스트마다 자동 적용...override_db를 parameter로 항상 안써도 된다.
def override_db(test_db): #위의 test_db주입
    def _get_db():
        try:
            yield test_db
        finally:
            pass
    app.dependency_overrides[get_db] = _get_db #의존성 바꿔치기
    yield #실행
    app.dependency_overrides.clear() #테스트 끝난후 override 해제, 다시 원래 DB로 복구


#테스트용 클라이언트
@pytest.fixture
def test_client():
    return TestClient(app=app)


#카테고리 1개 샘플
@pytest.fixture
def sample_category(test_db):
    catagory = Category(name="deep learning", description="deep learning is...")
    test_db.add(catagory)
    test_db.commit()
    test_db.refresh(catagory)
    return catagory


#도서 1개 샘플
@pytest.fixture
def sample_book(test_db, sample_category):
    book = Book(
        title="deep learning",
        author="jskim",
        isbn="1",
        price=30000,
        stock_quantity=10,
        category_id=sample_category.id,
    )
    test_db.add(book)
    test_db.commit()
    test_db.refresh(book)
    return book
