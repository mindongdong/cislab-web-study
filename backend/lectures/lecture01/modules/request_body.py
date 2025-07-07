"""
요청 본문 (Request Body) 및 고급 유효성 검사 학습 모듈

강의 내용:
1. Pydantic BaseModel을 사용한 요청 본문 처리
2. 경로/쿼리 매개변수와 요청 본문 조합
3. 다중 본문 매개변수
4. Body()를 사용한 단일 값 처리
5. Field를 활용한 모델 필드 검증
6. 요청 예제 데이터 선언
"""

from typing import Optional, List, Union
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field, EmailStr, validator
from enum import Enum

# 라우터 생성
router = APIRouter()

# Enum 정의
class UserRole(str, Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

# 1. 기본 Pydantic 모델들

class User(BaseModel):
    """기본 사용자 모델"""
    name: str = Field(..., min_length=2, max_length=50, description="사용자 이름")
    email: str = Field(..., description="이메일 주소")
    age: Optional[int] = Field(None, ge=0, le=150, description="나이 (0-150)")
    role: UserRole = Field(UserRole.user, description="사용자 역할")
    bio: Optional[str] = Field(None, max_length=500, description="자기소개")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "홍길동",
                "email": "hong@example.com",
                "age": 30,
                "role": "user",
                "bio": "안녕하세요, 홍길동입니다."
            }
        }

class UserCreate(BaseModel):
    """사용자 생성용 모델 (비밀번호 포함)"""
    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8, description="비밀번호 (최소 8자)")
    age: Optional[int] = Field(None, ge=13, le=150, description="나이 (13-150)")
    role: UserRole = UserRole.user
    terms_accepted: bool = Field(..., description="이용약관 동의 여부")
    
    @validator('password')
    def validate_password(cls, v):
        """비밀번호 복잡도 검증"""
        if not any(c.isupper() for c in v):
            raise ValueError('비밀번호에는 최소 하나의 대문자가 포함되어야 합니다')
        if not any(c.islower() for c in v):
            raise ValueError('비밀번호에는 최소 하나의 소문자가 포함되어야 합니다')
        if not any(c.isdigit() for c in v):
            raise ValueError('비밀번호에는 최소 하나의 숫자가 포함되어야 합니다')
        return v
    
    @validator('terms_accepted')
    def validate_terms(cls, v):
        """이용약관 동의 검증"""
        if not v:
            raise ValueError('이용약관에 동의해야 합니다')
        return v

class UserUpdate(BaseModel):
    """사용자 수정용 모델 (모든 필드 선택적)"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = Field(None, regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    age: Optional[int] = Field(None, ge=13, le=150)
    bio: Optional[str] = Field(None, max_length=500)

class Task(BaseModel):
    """작업 모델"""
    title: str = Field(..., min_length=1, max_length=200, description="작업 제목")
    description: Optional[str] = Field(None, max_length=1000, description="작업 설명")
    priority: Priority = Field(Priority.medium, description="우선순위")
    due_date: Optional[str] = Field(None, description="마감일 (YYYY-MM-DD)")
    tags: List[str] = Field(default=[], description="태그 목록")
    estimated_hours: Optional[float] = Field(None, gt=0, le=100, description="예상 소요 시간")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "일반 작업 예시",
                    "description": "일반적인 작업 생성 예시입니다",
                    "value": {
                        "title": "API 문서 작성",
                        "description": "FastAPI 프로젝트의 API 문서를 작성합니다",
                        "priority": "medium",
                        "due_date": "2024-02-01",
                        "tags": ["문서", "API", "FastAPI"],
                        "estimated_hours": 4.5
                    }
                },
                {
                    "summary": "긴급 작업 예시", 
                    "description": "높은 우선순위의 긴급 작업 예시입니다",
                    "value": {
                        "title": "버그 수정",
                        "description": "로그인 시스템의 중요한 버그를 수정합니다",
                        "priority": "high",
                        "due_date": "2024-01-20",
                        "tags": ["버그", "긴급", "로그인"],
                        "estimated_hours": 2.0
                    }
                }
            ]
        }

# 응답 모델들
class UserResponse(BaseModel):
    """사용자 응답 모델"""
    id: int
    name: str
    email: str
    age: Optional[int]
    role: str
    bio: Optional[str]
    created_at: str
    is_active: bool

class TaskResponse(BaseModel):
    """작업 응답 모델"""
    id: int
    title: str
    description: Optional[str]
    priority: str
    due_date: Optional[str]
    tags: List[str]
    estimated_hours: Optional[float]
    created_at: str
    user_id: int

# 2. 기본 요청 본문 예제

@router.get("/")
async def body_root():
    """요청 본문 모듈의 루트"""
    return {
        "message": "요청 본문 학습 모듈",
        "available_endpoints": [
            "POST /users - 사용자 생성",
            "PUT /users/{user_id} - 사용자 수정",
            "POST /users/{user_id}/tasks - 사용자의 작업 생성",
            "POST /multiple-body - 다중 본문 매개변수",
            "POST /with-metadata - 본문 + 추가 데이터"
        ]
    }

@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    사용자 생성 API
    - Pydantic 모델을 사용한 요청 본문 처리
    - 자동 유효성 검증 및 오류 메시지
    - 복잡한 비즈니스 로직 검증 (validator 사용)
    """
    # 이메일 중복 체크 시뮬레이션
    existing_emails = ["admin@example.com", "test@example.com"]
    if user.email in existing_emails:
        raise HTTPException(status_code=400, detail="이미 사용중인 이메일입니다")
    
    # 사용자 생성 시뮬레이션
    user_id = 12345  # 실제로는 데이터베이스에서 생성
    
    return UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        age=user.age,
        role=user.role.value,
        bio=None,  # 생성 시에는 bio 없음
        created_at=datetime.now().isoformat(),
        is_active=True
    )

# 3. 경로 매개변수와 요청 본문 조합

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    사용자 정보 수정 API
    - 경로 매개변수 (user_id)와 요청 본문 (user_update) 조합
    - 부분 업데이트 지원 (모든 필드 선택적)
    """
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="유효하지 않은 사용자 ID입니다")
    
    # 기존 사용자 조회 시뮬레이션
    existing_user = {
        "id": user_id,
        "name": "기존 사용자",
        "email": "existing@example.com", 
        "age": 25,
        "role": "user",
        "bio": "기존 자기소개",
        "created_at": "2024-01-01T00:00:00",
        "is_active": True
    }
    
    # 업데이트 적용
    update_data = user_update.dict(exclude_unset=True)  # None이 아닌 값만 가져오기
    
    for field, value in update_data.items():
        if field in existing_user:
            existing_user[field] = value
    
    return UserResponse(**existing_user)

@router.post("/users/{user_id}/tasks", response_model=TaskResponse)
async def create_task_for_user(
    user_id: int,
    task: Task,
    notify: bool = Body(False, description="알림 발송 여부")  # Body()로 추가 필드
):
    """
    특정 사용자의 작업 생성 API
    - 경로 매개변수 + 요청 본문 + Body()로 추가 단일 값
    """
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="유효하지 않은 사용자 ID입니다")
    
    # 마감일 유효성 검증
    if task.due_date:
        try:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d")
            if due_date.date() < datetime.now().date():
                raise HTTPException(status_code=400, detail="마감일은 현재 날짜 이후여야 합니다")
        except ValueError:
            raise HTTPException(status_code=400, detail="마감일 형식이 올바르지 않습니다 (YYYY-MM-DD)")
    
    # 작업 생성 시뮬레이션
    task_id = 67890
    
    response = TaskResponse(
        id=task_id,
        title=task.title,
        description=task.description,
        priority=task.priority.value,
        due_date=task.due_date,
        tags=task.tags,
        estimated_hours=task.estimated_hours,
        created_at=datetime.now().isoformat(),
        user_id=user_id
    )
    
    # 알림 발송 시뮬레이션
    if notify:
        return {
            "task": response,
            "notification": {
                "sent": True,
                "message": f"새로운 작업 '{task.title}'이 생성되었습니다",
                "channels": ["email", "push"]
            }
        }
    
    return response

# 4. 다중 본문 매개변수

class Project(BaseModel):
    """프로젝트 모델"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    budget: Optional[float] = Field(None, gt=0)
    
class Team(BaseModel):
    """팀 모델"""
    name: str = Field(..., min_length=1, max_length=50)
    members: List[str] = Field(..., min_items=1, description="팀 멤버 목록")
    lead: str = Field(..., description="팀 리더")

@router.post("/projects")
async def create_project_with_team(
    project: Project,
    team: Team,
    priority: int = Body(..., ge=1, le=5, description="프로젝트 우선순위 (1-5)")
):
    """
    프로젝트와 팀을 함께 생성하는 API
    - 다중 Pydantic 모델 (project, team)
    - Body()를 사용한 추가 단일 값 (priority)
    
    요청 본문 구조:
    {
        "project": { ... },
        "team": { ... },
        "priority": 3
    }
    """
    # 팀 리더가 멤버에 포함되어 있는지 확인
    if team.lead not in team.members:
        raise HTTPException(status_code=400, detail="팀 리더는 팀 멤버에 포함되어야 합니다")
    
    # 프로젝트 생성 시뮬레이션
    project_id = 11111
    team_id = 22222
    
    return {
        "project": {
            "id": project_id,
            "name": project.name,
            "description": project.description,
            "budget": project.budget,
            "priority": priority,
            "created_at": datetime.now().isoformat()
        },
        "team": {
            "id": team_id,
            "name": team.name,
            "members": team.members,
            "lead": team.lead,
            "size": len(team.members)
        },
        "assignment": {
            "project_id": project_id,
            "team_id": team_id,
            "assigned_at": datetime.now().isoformat()
        }
    }

# 5. Body(embed=True) 사용 예제

class Settings(BaseModel):
    """설정 모델"""
    theme: str = Field("light", regex="^(light|dark)$")
    language: str = Field("ko", regex="^(ko|en|ja)$")
    notifications: bool = Field(True)
    auto_save: bool = Field(True)
    timeout: int = Field(300, ge=60, le=3600, description="세션 타임아웃 (초)")

@router.post("/settings")
async def update_settings(
    settings: Settings = Body(..., embed=True)
):
    """
    설정 업데이트 API
    - Body(embed=True)를 사용하여 단일 모델을 본문 내 키로 래핑
    
    일반적인 요청: { "theme": "dark", ... }
    embed=True 요청: { "settings": { "theme": "dark", ... } }
    """
    return {
        "message": "설정이 성공적으로 업데이트되었습니다",
        "updated_settings": settings.dict(),
        "applied_at": datetime.now().isoformat(),
        "restart_required": settings.theme != "light"  # 다크모드 적용 시 재시작 필요
    }

# 6. Field를 활용한 고급 검증

class Product(BaseModel):
    """상품 모델 (Field를 활용한 상세 검증)"""
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        title="상품명",
        description="상품의 이름입니다"
    )
    price: float = Field(
        ..., 
        gt=0, 
        le=1000000,
        title="가격",
        description="상품 가격 (원화, 0초과 1,000,000 이하)"
    )
    category: str = Field(
        ...,
        regex="^[a-z_]+$",
        title="카테고리",
        description="소문자와 언더스코어만 허용되는 카테고리"
    )
    sku: str = Field(
        ...,
        min_length=8,
        max_length=12,
        regex="^[A-Z]{3}[0-9]{5,9}$",
        title="SKU",
        description="상품 코드 (대문자 3자 + 숫자 5-9자)"
    )
    weight: Optional[float] = Field(
        None,
        gt=0,
        le=1000,
        title="무게",
        description="상품 무게 (kg, 0초과 1000 이하)"
    )
    tags: List[str] = Field(
        default=[],
        max_items=10,
        title="태그",
        description="상품 태그 (최대 10개)"
    )
    
    @validator('tags')
    def validate_tags(cls, v):
        """태그 유효성 검증"""
        for tag in v:
            if len(tag) < 2 or len(tag) > 20:
                raise ValueError('각 태그는 2-20자 사이여야 합니다')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "name": "고급 노트북",
                "price": 1299999,
                "category": "electronics",
                "sku": "LAP123456",
                "weight": 2.5,
                "tags": ["노트북", "고성능", "게이밍"]
            }
        }

@router.post("/products")
async def create_product(product: Product):
    """
    상품 생성 API
    - Field를 활용한 상세한 유효성 검증
    - 복잡한 정규식 검증
    - 커스텀 validator 사용
    """
    # SKU 중복 체크 시뮬레이션
    existing_skus = ["LAP123456", "PHO987654", "TAB555555"]
    if product.sku in existing_skus:
        raise HTTPException(status_code=400, detail="이미 존재하는 SKU입니다")
    
    # 상품 생성 시뮬레이션
    product_id = 98765
    
    return {
        "id": product_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "sku": product.sku,
        "weight": product.weight,
        "tags": product.tags,
        "created_at": datetime.now().isoformat(),
        "status": "active",
        "inventory": {
            "stock": 0,
            "reserved": 0,
            "available": 0
        }
    }

# 7. 요청 예제 데이터가 풍부한 모델

class Order(BaseModel):
    """주문 모델 (다양한 예제 데이터 포함)"""
    customer_email: str = Field(..., description="고객 이메일")
    items: List[dict] = Field(..., min_items=1, description="주문 상품 목록")
    shipping_address: dict = Field(..., description="배송 주소")
    payment_method: str = Field(..., regex="^(card|bank|paypal)$", description="결제 방법")
    notes: Optional[str] = Field(None, max_length=200, description="주문 메모")
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "summary": "일반 주문",
                    "description": "일반적인 온라인 주문 예시",
                    "value": {
                        "customer_email": "customer@example.com",
                        "items": [
                            {"product_id": 1, "quantity": 2, "price": 29.99},
                            {"product_id": 2, "quantity": 1, "price": 59.99}
                        ],
                        "shipping_address": {
                            "street": "서울특별시 강남구 테헤란로 123",
                            "city": "서울",
                            "postal_code": "06234",
                            "country": "KR"
                        },
                        "payment_method": "card",
                        "notes": "빠른 배송 부탁드립니다"
                    }
                },
                {
                    "summary": "대량 주문",
                    "description": "기업 고객의 대량 주문 예시",
                    "value": {
                        "customer_email": "corporate@company.com",
                        "items": [
                            {"product_id": 10, "quantity": 50, "price": 15.99},
                            {"product_id": 11, "quantity": 30, "price": 25.99}
                        ],
                        "shipping_address": {
                            "street": "부산광역시 해운대구 센텀중앙로 456",
                            "city": "부산",
                            "postal_code": "48058",
                            "country": "KR"
                        },
                        "payment_method": "bank",
                        "notes": "세금계산서 발행 필요"
                    }
                }
            ]
        }

@router.post("/orders")
async def create_order(order: Order):
    """
    주문 생성 API
    - 다양한 예제 데이터를 포함한 복합 모델
    - 중첩된 딕셔너리와 리스트 처리
    """
    # 주문 유효성 검증
    total_amount = sum(item.get("price", 0) * item.get("quantity", 0) for item in order.items)
    
    if total_amount <= 0:
        raise HTTPException(status_code=400, detail="주문 금액이 0보다 커야 합니다")
    
    # 주문 생성 시뮬레이션
    order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "order_id": order_id,
        "customer_email": order.customer_email,
        "items": order.items,
        "shipping_address": order.shipping_address,
        "payment_method": order.payment_method,
        "notes": order.notes,
        "total_amount": total_amount,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "estimated_delivery": "2024-01-25T18:00:00"
    }