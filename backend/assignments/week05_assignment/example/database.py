"""
데이터베이스 연결 설정
- 세션 관리와 Base 클래스 정의
- 트랜잭션 처리를 위한 의존성 주입 함수
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 데이터베이스 URL 구성
# 실제 운영에서는 환경 변수로 관리하는 것이 보안상 중요합니다
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/book_management"
)

# SQLAlchemy 엔진 생성
# pool_pre_ping=True: 연결 상태를 체크하여 끊어진 연결 자동 재연결
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=True  # 개발 시 SQL 쿼리 로깅 (운영에서는 False)
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,  # 명시적 커밋 사용
    autoflush=False,   # 자동 flush 비활성화로 성능 최적화
    bind=engine
)

# ORM 모델의 베이스 클래스
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    데이터베이스 세션을 제공하는 의존성 주입 함수
    - FastAPI의 Depends와 함께 사용
    - 요청 처리 후 자동으로 세션 종료
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
