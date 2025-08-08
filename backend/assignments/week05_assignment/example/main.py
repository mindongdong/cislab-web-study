"""
FastAPI 애플리케이션 메인 진입점
- 미들웨어 설정
- 라우터 등록
- 예외 핸들러 설정
- 데이터베이스 초기화
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.database import engine, Base
from app.routers import books, categories
from app.utils.exceptions import BusinessException
import uvicorn

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="도서 관리 시스템 API",
    description="FastAPI와 SQLAlchemy를 활용한 도서 관리 RESTful API",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS 미들웨어 설정 (개발 환경용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 운영 환경에서는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(books.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")

# 전역 예외 핸들러
@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """비즈니스 로직 예외 처리"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "data": None
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Pydantic 유효성 검증 오류 처리"""
    errors = exc.errors()
    error_messages = []
    
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"][1:])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "입력 데이터가 유효하지 않습니다",
            "data": {"details": error_messages}
        }
    )

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """일반 HTTP 예외 처리"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.detail if isinstance(exc.detail, str) else exc.detail.get("message", "오류가 발생했습니다"),
            "data": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """예상치 못한 예외 처리"""
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "서버 내부 오류가 발생했습니다",
            "data": None
        }
    )

# 루트 엔드포인트
@app.get("/")
async def root():
    """API 상태 확인"""
    return {
        "status": "success",
        "message": "도서 관리 시스템 API가 정상적으로 실행 중입니다",
        "data": {
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "success",
        "message": "서비스가 정상 작동 중입니다",
        "data": {"status": "healthy"}
    }

if __name__ == "__main__":
    # 개발 서버 실행
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # 코드 변경 시 자동 재시작
    )