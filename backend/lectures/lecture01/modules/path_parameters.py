"""
경로 매개변수 (Path Parameters) 학습 모듈

강의 내용:
1. 경로 매개변수 기본 사용법
2. 타입 트와 자동 변환
3. Enum을 사용한 사전 정의 값
4. 경로를 포함하는 매개변수
5. 경로 작동 순서의 중요성
"""

from enum import Enum
from typing import Optional
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel

# 라우터 생성
router = APIRouter()

# 1. Enum을 사용한 사전 정의 값
class ModelName(str, Enum):
    """머신러닝 모델 이름을 위한 Enum"""
    alexnet = "alexnet"
    resnet = "resnet" 
    lenet = "lenet"

class ItemType(str, Enum):
    """아이템 타입을 위한 Enum"""
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    food = "food"

# 응답 모델 정의
class Item(BaseModel):
    item_id: int
    name: str
    description: Optional[str] = None
    price: float
    category: str

class FileInfo(BaseModel):
    file_path: str
    exists: bool
    size: Optional[int] = None
    extension: Optional[str] = None

class ModelInfo(BaseModel):
    model_name: str
    description: str
    parameters: int
    accuracy: float

# 2. 기본 경로 매개변수 예제들

@router.get("/")
async def path_root():
    """경로 매개변수 모듈의 루트"""
    return {
        "message": "경로 매개변수 학습 모듈",
        "available_endpoints": [
            "/items/{item_id} - 아이템 조회",
            "/users/{user_id} - 사용자 조회", 
            "/models/{model_name} - 모델 정보 조회",
            "/categories/{category}/items/{item_id} - 카테고리별 아이템",
            "/files/{file_path:path} - 파일 경로 처리"
        ]
    }

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    """
    기본 경로 매개변수 예제
    - item_id는 자동으로 int 타입으로 변환됩니다
    - 유효하지 않은 값이 오면 자동으로 오류 응답을 반환합니다
    """
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Item ID는 1 이상이어야 합니다")
    
    # 실제로는 데이터베이스에서 조회하겠지만, 여기서는 예시 데이터 반환
    sample_items = {
        1: {"name": "노트북", "description": "고성능 노트북", "price": 1299.99, "category": "electronics"},
        2: {"name": "티셔츠", "description": "편안한 면 티셔츠", "price": 29.99, "category": "clothing"},
        3: {"name": "파이썬 책", "description": "파이썬 프로그래밍 입문서", "price": 39.99, "category": "books"}
    }
    
    if item_id in sample_items:
        item_data = sample_items[item_id]
        return Item(
            item_id=item_id,
            name=item_data["name"],
            description=item_data["description"],
            price=item_data["price"],
            category=item_data["category"]
        )
    else:
        # 존재하지 않는 아이템의 경우 예시 데이터 생성
        return Item(
            item_id=item_id,
            name=f"상품 {item_id}",
            description=f"상품 {item_id}에 대한 설명",
            price=99.99,
            category="general"
        )

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """
    문자열 경로 매개변수 예제
    - user_id는 문자열로 처리됩니다
    """
    return {
        "user_id": user_id,
        "username": f"user_{user_id}",
        "email": f"{user_id}@example.com",
        "profile": {
            "display_name": f"사용자 {user_id}",
            "join_date": "2024-01-01",
            "status": "active"
        }
    }

# 3. 경로 작동 순서의 중요성 (고정 경로가 먼저 와야 함)

@router.get("/users/me")
async def get_current_user():
    """
    현재 사용자 정보 조회 (고정 경로)
    주의: 이 엔드포인트는 /users/{user_id}보다 먼저 정의되어야 합니다!
    그렇지 않으면 /users/me가 user_id="me"로 처리됩니다.
    """
    return {
        "user_id": "current",
        "username": "current_user",
        "email": "current@example.com",
        "is_current": True,
        "permissions": ["read", "write", "admin"]
    }

@router.get("/users/admin")
async def get_admin_info():
    """관리자 정보 조회 (고정 경로)"""
    return {
        "user_type": "admin",
        "admin_level": "super",
        "permissions": ["all"],
        "dashboard_url": "/admin/dashboard"
    }

# 4. Enum을 사용한 사전 정의 값

@router.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    Enum을 사용한 경로 매개변수
    - 미리 정의된 값만 허용됩니다
    - API 문서에 가능한 값들이 자동으로 표시됩니다
    """
    model_info = {
        ModelName.alexnet: {
            "description": "AlexNet은 2012년 ImageNet 대회에서 우승한 CNN 모델입니다",
            "parameters": 60_000_000,
            "accuracy": 0.847
        },
        ModelName.resnet: {
            "description": "ResNet은 깊은 신경망에서 발생하는 기울기 소실 문제를 해결한 모델입니다",
            "parameters": 25_000_000,
            "accuracy": 0.923
        },
        ModelName.lenet: {
            "description": "LeNet은 최초의 CNN 모델 중 하나로 손글씨 인식에 사용되었습니다",
            "parameters": 60_000,
            "accuracy": 0.782
        }
    }
    
    info = model_info[model_name]
    return ModelInfo(
        model_name=model_name.value,  # Enum의 실제 문자열 값
        description=info["description"],
        parameters=info["parameters"],
        accuracy=info["accuracy"]
    )

# 5. 여러 경로 매개변수 조합

@router.get("/categories/{category}/items/{item_id}")
async def get_item_by_category(
    category: ItemType, 
    item_id: int = Path(..., ge=1, description="아이템 ID (1 이상)")
):
    """
    여러 경로 매개변수를 조합한 예제
    - category: Enum으로 제한된 카테고리
    - item_id: 숫자 검증이 포함된 아이템 ID
    """
    # 카테고리별 설명
    category_descriptions = {
        ItemType.electronics: "전자제품",
        ItemType.clothing: "의류",
        ItemType.books: "도서",
        ItemType.food: "식품"
    }
    
    return {
        "item_id": item_id,
        "category": category.value,
        "category_description": category_descriptions[category],
        "item_details": {
            "name": f"{category_descriptions[category]} 상품 {item_id}",
            "category_specific_info": f"{category.value} 카테고리의 특별 정보",
            "url": f"/categories/{category.value}/items/{item_id}"
        }
    }

# 6. 경로를 포함하는 경로 매개변수

@router.get("/files/{file_path:path}")
async def get_file_info(file_path: str):
    """
    파일 경로를 포함하는 경로 매개변수
    - file_path:path를 사용하여 슬래시(/)가 포함된 경로를 처리합니다
    - 예: /files/docs/tutorials/fastapi.md
    """
    import os
    
    # 파일 확장자 추출
    extension = None
    if '.' in file_path:
        extension = file_path.split('.')[-1].lower()
    
    # 예시 파일 크기 (실제로는 파일 시스템에서 조회)
    fake_file_sizes = {
        "docs/readme.md": 1024,
        "docs/tutorial.md": 2048,
        "images/logo.png": 4096,
        "scripts/main.py": 512
    }
    
    file_size = fake_file_sizes.get(file_path, None)
    file_exists = file_path in fake_file_sizes
    
    return FileInfo(
        file_path=file_path,
        exists=file_exists,
        size=file_size,
        extension=extension
    )

# 7. 경로 매개변수와 추가 정보

@router.get("/products/{product_id}/reviews/{review_id}")
async def get_product_review(
    product_id: int = Path(..., ge=1, description="상품 ID"),
    review_id: int = Path(..., ge=1, description="리뷰 ID")
):
    """중첩된 리소스 관계를 표현하는 경로"""
    return {
        "product_id": product_id,
        "review_id": review_id,
        "review": {
            "title": f"상품 {product_id}에 대한 리뷰 {review_id}",
            "rating": 4.5,
            "content": "이 상품은 정말 좋습니다!",
            "author": "만족한고객",
            "created_at": "2024-01-15T10:30:00"
        },
        "product_info": {
            "name": f"상품 {product_id}",
            "total_reviews": 15,
            "average_rating": 4.2
        }
    }

# 8. 경로 매개변수 종합 예제

@router.get("/api/v1/{service}/{version}/{resource_id}")
async def get_versioned_resource(
    service: str = Path(..., pattern="^[a-z]+$", description="서비스 이름 (소문자만)"),
    version: str = Path(..., pattern="^v[0-9]+$", description="API 버전 (v1, v2 등)"),
    resource_id: str = Path(..., min_length=1, max_length=50, description="리소스 ID")
):
    """
    복잡한 API 버전 관리를 위한 경로 매개변수 예제
    - 정규식을 사용한 검증
    - 문자열 길이 제한
    """
    return {
        "service": service,
        "version": version,
        "resource_id": resource_id,
        "endpoint": f"/api/v1/{service}/{version}/{resource_id}",
        "metadata": {
            "service_description": f"{service} 서비스",
            "version_info": f"API {version}",
            "resource_type": "dynamic",
            "supported_methods": ["GET", "POST", "PUT", "DELETE"]
        }
    }