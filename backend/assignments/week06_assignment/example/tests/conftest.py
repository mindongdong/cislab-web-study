"""
테스트 설정 및 공통 픽스처
- 테스트 데이터베이스 설정
- 클라이언트 픽스처
- 모의 데이터 생성 픽스처
"""
import os
import sys
import pytest
import tempfile
from typing import Generator, Any
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, Session
from unittest.mock import Mock

# Add week05 assignment path to sys.path for imports
week05_example_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "week05_assignment", "example"))
if week05_example_path not in sys.path:
    sys.path.insert(0, week05_example_path)

# 테스트용 환경 변수 설정
os.environ["TESTING"] = "1"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

# Import from week05 with app namespace
from main import app
from database import get_db, Base
from models.book import Book
from models.category import Category


# 테스트 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,  # SQLite 전용 옵션
    },
    poolclass=StaticPool,  # 메모리 DB에서 연결 풀 사용
)

TestingSessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=test_engine
)


@pytest.fixture(scope="session")
def test_db_engine():
    """
    세션 스코프 DB 엔진 픽스처
    - 테스트 세션 동안 하나의 엔진 사용
    """
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(test_db_engine) -> Generator[Session, None, None]:
    """
    함수 스코프 DB 세션 픽스처
    - 각 테스트마다 독립적인 세션
    - 테스트 종료 후 롤백으로 격리 보장
    """
    connection = test_db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def test_client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    테스트 클라이언트 픽스처
    - FastAPI 애플리케이션 테스트용 클라이언트
    - DB 의존성 오버라이드
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()


# 테스트 데이터 픽스처들
@pytest.fixture
def sample_category(db_session: Session) -> Category:
    """샘플 카테고리 픽스처"""
    category = Category(
        name="프로그래밍",
        description="프로그래밍 관련 도서"
    )
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture
def sample_categories(db_session: Session) -> list[Category]:
    """다중 카테고리 픽스처"""
    categories = [
        Category(name="프로그래밍", description="프로그래밍 관련 도서"),
        Category(name="데이터베이스", description="데이터베이스 관련 도서"),
        Category(name="웹개발", description="웹개발 관련 도서"),
    ]
    
    for category in categories:
        db_session.add(category)
    
    db_session.commit()
    
    for category in categories:
        db_session.refresh(category)
    
    return categories


@pytest.fixture
def sample_book(db_session: Session, sample_category: Category) -> Book:
    """샘플 도서 픽스처"""
    from datetime import date
    
    book = Book(
        title="Clean Code",
        author="Robert C. Martin",
        isbn="9780132350884",
        price=35000,
        stock_quantity=10,
        published_date=date(2008, 8, 1),
        category_id=sample_category.id
    )
    
    db_session.add(book)
    db_session.commit()
    db_session.refresh(book)
    return book


@pytest.fixture
def sample_books(db_session: Session, sample_categories: list[Category]) -> list[Book]:
    """다중 도서 픽스처"""
    from datetime import date
    
    books = [
        Book(
            title="Clean Code",
            author="Robert C. Martin",
            isbn="9780132350884",
            price=35000,
            stock_quantity=10,
            published_date=date(2008, 8, 1),
            category_id=sample_categories[0].id
        ),
        Book(
            title="Python Crash Course",
            author="Eric Matthes",
            isbn="9781593279288",
            price=28000,
            stock_quantity=5,
            published_date=date(2019, 5, 3),
            category_id=sample_categories[0].id
        ),
        Book(
            title="Database System Concepts",
            author="Abraham Silberschatz",
            isbn="9780078022159",
            price=45000,
            stock_quantity=3,
            published_date=date(2019, 2, 19),
            category_id=sample_categories[1].id
        ),
    ]
    
    for book in books:
        db_session.add(book)
    
    db_session.commit()
    
    for book in books:
        db_session.refresh(book)
    
    return books


# 모킹용 픽스처들
@pytest.fixture
def mock_external_service():
    """외부 서비스 모킹 픽스처"""
    return Mock()


@pytest.fixture
def mock_email_service():
    """이메일 서비스 모킹 픽스처"""
    mock = Mock()
    mock.send_notification.return_value = {"status": "sent", "message_id": "12345"}
    return mock


@pytest.fixture
def mock_isbn_validator():
    """ISBN 검증 서비스 모킹 픽스처"""
    mock = Mock()
    mock.validate_isbn.return_value = True
    mock.get_book_info.return_value = {
        "title": "Mocked Book",
        "author": "Mocked Author",
        "publisher": "Mocked Publisher"
    }
    return mock


# 테스트 데이터 생성 헬퍼
@pytest.fixture
def book_factory(db_session: Session):
    """도서 팩토리 픽스처"""
    def create_book(**kwargs):
        from datetime import date
        
        defaults = {
            "title": "Test Book",
            "author": "Test Author",
            "isbn": "9781234567890",
            "price": 25000,
            "stock_quantity": 5,
            "published_date": date.today(),
            "category_id": None
        }
        defaults.update(kwargs)
        
        book = Book(**defaults)
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        return book
    
    return create_book


@pytest.fixture
def category_factory(db_session: Session):
    """카테고리 팩토리 픽스처"""
    def create_category(**kwargs):
        defaults = {
            "name": "Test Category",
            "description": "Test Description"
        }
        defaults.update(kwargs)
        
        category = Category(**defaults)
        db_session.add(category)
        db_session.commit()
        db_session.refresh(category)
        return category
    
    return create_category


# 테스트 환경 관리
@pytest.fixture(autouse=True)
def setup_test_environment():
    """
    테스트 환경 자동 설정
    - 모든 테스트에 자동 적용
    - 테스트 전후 환경 정리
    """
    # 테스트 시작 전 설정
    original_db_url = os.environ.get("DATABASE_URL")
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    
    yield
    
    # 테스트 종료 후 정리
    if original_db_url:
        os.environ["DATABASE_URL"] = original_db_url
    elif "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]


# 성능 테스트용 픽스처
@pytest.fixture
def large_dataset(db_session: Session, sample_categories: list[Category]):
    """대용량 테스트 데이터셋"""
    from datetime import date, timedelta
    import random
    
    books = []
    base_date = date(2020, 1, 1)
    
    for i in range(100):
        book = Book(
            title=f"Test Book {i:03d}",
            author=f"Author {i % 10}",
            isbn=f"978{i:010d}",
            price=random.randint(15000, 50000),
            stock_quantity=random.randint(0, 20),
            published_date=base_date + timedelta(days=i),
            category_id=sample_categories[i % len(sample_categories)].id
        )
        books.append(book)
    
    db_session.add_all(books)
    db_session.commit()
    
    return books