"""
중첩 모델 (Nested Models) 학습 모듈

강의 내용:
1. Pydantic의 중첩 모델 지원
2. 리스트 필드와 타입 명시
3. 집합(Set) 타입 사용
4. 중첩 모델 정의
5. 특별한 타입 및 검증 (HttpUrl 등)
6. 서브모델 리스트
7. 깊게 중첩된 모델
8. dict 본문 처리
"""

from typing import List, Set, Optional, Dict, Union
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, validator
from fastapi import APIRouter, HTTPException
from enum import Enum

# 라우터 생성
router = APIRouter()

# Enum 정의
class ImageType(str, Enum):
    jpeg = "jpeg"
    png = "png"
    gif = "gif"
    webp = "webp"

class ItemStatus(str, Enum):
    draft = "draft"
    published = "published"
    archived = "archived"

# 1. 기본 중첩 모델들

class Image(BaseModel):
    """이미지 모델"""
    url: HttpUrl = Field(..., description="이미지 URL")
    name: str = Field(..., min_length=1, max_length=100, description="이미지 이름")
    type: ImageType = Field(..., description="이미지 타입")
    size: Optional[int] = Field(None, gt=0, description="파일 크기 (bytes)")
    alt_text: Optional[str] = Field(None, max_length=200, description="대체 텍스트")
    
    class Config:
        schema_extra = {
            "example": {
                "url": "https://example.com/image.jpg",
                "name": "상품 이미지",
                "type": "jpeg",
                "size": 1024000,
                "alt_text": "고품질 노트북 이미지"
            }
        }

class Tag(BaseModel):
    """태그 모델"""
    name: str = Field(..., min_length=1, max_length=30, description="태그 이름")
    color: Optional[str] = Field(None, regex="^#[0-9A-Fa-f]{6}$", description="태그 색상 (hex)")
    
class Category(BaseModel):
    """카테고리 모델"""
    id: int = Field(..., gt=0, description="카테고리 ID")
    name: str = Field(..., min_length=1, max_length=50, description="카테고리 이름")
    parent_id: Optional[int] = Field(None, gt=0, description="상위 카테고리 ID")

class Item(BaseModel):
    """상품 모델 (중첩 모델 포함)"""
    name: str = Field(..., min_length=1, max_length=100, description="상품명")
    description: Optional[str] = Field(None, max_length=1000, description="상품 설명")
    price: float = Field(..., gt=0, description="가격")
    tax: Optional[float] = Field(None, ge=0, description="세금")
    tags: Set[str] = Field(default=set(), description="태그 집합 (중복 제거)")
    images: List[Image] = Field(default=[], description="상품 이미지 목록")
    category: Optional[Category] = Field(None, description="카테고리 정보")
    metadata: Dict[str, Union[str, int, float]] = Field(default={}, description="추가 메타데이터")
    status: ItemStatus = Field(ItemStatus.draft, description="상품 상태")
    
    @validator('tags')
    def validate_tags(cls, v):
        """태그 개수 제한"""
        if len(v) > 10:
            raise ValueError('태그는 최대 10개까지 허용됩니다')
        return v
    
    @validator('images')
    def validate_images(cls, v):
        """이미지 개수 제한"""
        if len(v) > 20:
            raise ValueError('이미지는 최대 20개까지 허용됩니다')
        return v

# 2. 깊게 중첩된 모델

class Address(BaseModel):
    """주소 모델"""
    street: str = Field(..., min_length=1, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: str = Field(..., min_length=3, max_length=20)
    country: str = Field(..., min_length=2, max_length=3, description="국가 코드 (KR, US 등)")

class Contact(BaseModel):
    """연락처 모델"""
    email: str = Field(..., regex="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    phone: Optional[str] = Field(None, regex="^[0-9+-]+$", description="전화번호")
    website: Optional[HttpUrl] = Field(None, description="웹사이트")

class Company(BaseModel):
    """회사 모델"""
    name: str = Field(..., min_length=1, max_length=200)
    registration_number: Optional[str] = Field(None, description="사업자등록번호")
    address: Address = Field(..., description="회사 주소")
    contact: Contact = Field(..., description="연락처 정보")

class Seller(BaseModel):
    """판매자 모델"""
    name: str = Field(..., min_length=1, max_length=100)
    company: Optional[Company] = Field(None, description="회사 정보")
    personal_contact: Contact = Field(..., description="개인 연락처")
    verified: bool = Field(False, description="인증 여부")
    rating: Optional[float] = Field(None, ge=0, le=5, description="평점 (0-5)")

class Offer(BaseModel):
    """상품 제안 모델 (깊게 중첩된 구조)"""
    name: str = Field(..., min_length=1, max_length=200, description="제안명")
    description: Optional[str] = Field(None, max_length=2000, description="제안 설명")
    items: List[Item] = Field(..., min_items=1, description="포함된 상품 목록")
    seller: Seller = Field(..., description="판매자 정보")
    total_price: Optional[float] = Field(None, gt=0, description="총 가격")
    discount_percentage: Optional[float] = Field(None, ge=0, le=100, description="할인율")
    valid_until: Optional[str] = Field(None, description="유효기간 (ISO 날짜)")
    terms_and_conditions: List[str] = Field(default=[], description="이용약관 목록")
    
    @validator('total_price', always=True)
    def calculate_total_price(cls, v, values):
        """총 가격 자동 계산"""
        if 'items' in values and values['items']:
            calculated_price = sum(item.price for item in values['items'])
            if 'discount_percentage' in values and values['discount_percentage']:
                calculated_price *= (1 - values['discount_percentage'] / 100)
            return calculated_price
        return v

# 3. 응답 모델들

class ItemResponse(BaseModel):
    """상품 응답 모델"""
    id: int
    name: str
    description: Optional[str]
    price: float
    tax: Optional[float]
    final_price: float  # 세금 포함 가격
    tags: Set[str]
    images: List[Image]
    category: Optional[Category]
    metadata: Dict[str, Union[str, int, float]]
    status: str
    created_at: str

class OfferResponse(BaseModel):
    """제안 응답 모델"""
    id: int
    name: str
    description: Optional[str]
    items: List[ItemResponse]
    seller: Seller
    total_price: float
    discount_percentage: Optional[float]
    final_price: float
    valid_until: Optional[str]
    terms_and_conditions: List[str]
    created_at: str
    items_count: int

# 4. API 엔드포인트들

@router.get("/")
async def nested_root():
    """중첩 모델 모듈의 루트"""
    return {
        "message": "중첩 모델 학습 모듈",
        "available_endpoints": [
            "POST /items - 상품 생성 (중첩 모델)",
            "POST /offers - 제안 생성 (깊게 중첩된 모델)",
            "POST /bulk-items - 여러 상품 일괄 생성",
            "POST /flexible-data - 유연한 데이터 구조",
            "GET /examples - 예시 데이터 확인"
        ],
        "model_structure": {
            "simple_nesting": "Item -> Image, Category",
            "deep_nesting": "Offer -> Seller -> Company -> Address, Contact",
            "collections": "List[Item], Set[str], Dict[str, Any]"
        }
    }

@router.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    """
    상품 생성 API
    - 중첩 모델 (Image, Category) 사용
    - 리스트와 집합 타입 처리
    - 딕셔너리 메타데이터 처리
    """
    # 카테고리 존재 여부 확인 시뮬레이션
    if item.category and item.category.id > 1000:
        raise HTTPException(status_code=400, detail="존재하지 않는 카테고리입니다")
    
    # 이미지 URL 유효성 추가 검증
    for image in item.images:
        if "example.com" in str(image.url):  # 예시 URL 금지
            raise HTTPException(status_code=400, detail="실제 이미지 URL을 사용해주세요")
    
    # 상품 ID 생성 시뮬레이션
    item_id = 12345
    
    # 최종 가격 계산 (세금 포함)
    final_price = item.price
    if item.tax:
        final_price += item.tax
    
    return ItemResponse(
        id=item_id,
        name=item.name,
        description=item.description,
        price=item.price,
        tax=item.tax,
        final_price=final_price,
        tags=item.tags,
        images=item.images,
        category=item.category,
        metadata=item.metadata,
        status=item.status.value,
        created_at=datetime.now().isoformat()
    )

@router.post("/offers", response_model=OfferResponse)
async def create_offer(offer: Offer):
    """
    제안 생성 API
    - 깊게 중첩된 모델 구조
    - 복잡한 비즈니스 로직 검증
    - 자동 계산 필드
    """
    # 판매자 인증 확인
    if not offer.seller.verified:
        raise HTTPException(status_code=400, detail="인증된 판매자만 제안을 생성할 수 있습니다")
    
    # 유효기간 검증
    if offer.valid_until:
        try:
            valid_date = datetime.fromisoformat(offer.valid_until.replace('Z', '+00:00'))
            if valid_date <= datetime.now():
                raise HTTPException(status_code=400, detail="유효기간이 현재 시각보다 이후여야 합니다")
        except ValueError:
            raise HTTPException(status_code=400, detail="유효기간 형식이 올바르지 않습니다")
    
    # 제안 ID 생성
    offer_id = 98765
    
    # 개별 상품 응답 생성
    item_responses = []
    for i, item in enumerate(offer.items):
        final_price = item.price
        if item.tax:
            final_price += item.tax
            
        item_responses.append(ItemResponse(
            id=50000 + i,
            name=item.name,
            description=item.description,
            price=item.price,
            tax=item.tax,
            final_price=final_price,
            tags=item.tags,
            images=item.images,
            category=item.category,
            metadata=item.metadata,
            status=item.status.value,
            created_at=datetime.now().isoformat()
        ))
    
    # 최종 가격 계산
    total_price = offer.total_price or sum(item.price for item in offer.items)
    final_price = total_price
    if offer.discount_percentage:
        final_price = total_price * (1 - offer.discount_percentage / 100)
    
    return OfferResponse(
        id=offer_id,
        name=offer.name,
        description=offer.description,
        items=item_responses,
        seller=offer.seller,
        total_price=total_price,
        discount_percentage=offer.discount_percentage,
        final_price=final_price,
        valid_until=offer.valid_until,
        terms_and_conditions=offer.terms_and_conditions,
        created_at=datetime.now().isoformat(),
        items_count=len(offer.items)
    )

# 5. 여러 상품 일괄 생성

class BulkItemRequest(BaseModel):
    """여러 상품 일괄 생성 요청"""
    items: List[Item] = Field(..., min_items=1, max_items=50, description="상품 목록 (최대 50개)")
    default_category: Optional[Category] = Field(None, description="기본 카테고리")
    apply_bulk_discount: bool = Field(False, description="대량 할인 적용 여부")
    
class BulkItemResponse(BaseModel):
    """여러 상품 일괄 생성 응답"""
    success_count: int
    failed_count: int
    created_items: List[ItemResponse]
    failed_items: List[Dict[str, str]]
    bulk_discount_applied: Optional[float]
    total_value: float

@router.post("/bulk-items", response_model=BulkItemResponse)
async def create_bulk_items(request: BulkItemRequest):
    """
    여러 상품 일괄 생성 API
    - 리스트 내 여러 복잡한 모델 처리
    - 부분 성공/실패 처리
    """
    created_items = []
    failed_items = []
    total_value = 0
    
    for i, item in enumerate(request.items):
        try:
            # 기본 카테고리 적용
            if not item.category and request.default_category:
                item.category = request.default_category
            
            # 상품 검증 및 생성 시뮬레이션
            if len(item.name) < 2:
                raise ValueError("상품명이 너무 짧습니다")
            
            # 대량 할인 적용
            price = item.price
            if request.apply_bulk_discount and len(request.items) >= 10:
                price *= 0.95  # 5% 할인
            
            final_price = price
            if item.tax:
                final_price += item.tax
            
            item_response = ItemResponse(
                id=70000 + i,
                name=item.name,
                description=item.description,
                price=price,
                tax=item.tax,
                final_price=final_price,
                tags=item.tags,
                images=item.images,
                category=item.category,
                metadata=item.metadata,
                status=item.status.value,
                created_at=datetime.now().isoformat()
            )
            
            created_items.append(item_response)
            total_value += final_price
            
        except Exception as e:
            failed_items.append({
                "index": i,
                "item_name": item.name,
                "error": str(e)
            })
    
    bulk_discount = 5.0 if request.apply_bulk_discount and len(request.items) >= 10 else None
    
    return BulkItemResponse(
        success_count=len(created_items),
        failed_count=len(failed_items),
        created_items=created_items,
        failed_items=failed_items,
        bulk_discount_applied=bulk_discount,
        total_value=total_value
    )

# 6. 유연한 데이터 구조 (Dict 본문)

@router.post("/flexible-data")
async def process_flexible_data(
    data: Dict[str, Union[str, int, float, List, Dict]] = Field(..., description="유연한 데이터 구조")
):
    """
    유연한 데이터 구조 처리 API
    - Dict를 사용한 동적 데이터 구조
    - 런타임에 데이터 구조 분석
    """
    analysis = {
        "received_keys": list(data.keys()),
        "data_types": {key: type(value).__name__ for key, value in data.items()},
        "total_keys": len(data),
        "processed_at": datetime.now().isoformat()
    }
    
    # 특별한 키들 처리
    special_processing = {}
    
    if "config" in data and isinstance(data["config"], dict):
        special_processing["config_keys"] = list(data["config"].keys())
    
    if "items" in data and isinstance(data["items"], list):
        special_processing["items_count"] = len(data["items"])
    
    if "metadata" in data:
        special_processing["metadata_type"] = type(data["metadata"]).__name__
    
    # 숫자 값들 합계 계산
    numeric_values = [v for v in data.values() if isinstance(v, (int, float))]
    if numeric_values:
        special_processing["numeric_sum"] = sum(numeric_values)
        special_processing["numeric_average"] = sum(numeric_values) / len(numeric_values)
    
    return {
        "original_data": data,
        "analysis": analysis,
        "special_processing": special_processing,
        "message": "유연한 데이터 구조가 성공적으로 처리되었습니다"
    }

# 7. 예시 데이터 확인

@router.get("/examples")
async def get_examples():
    """
    중첩 모델의 예시 데이터 제공
    클라이언트에서 테스트할 때 참고할 수 있는 샘플 데이터
    """
    return {
        "simple_item": {
            "name": "노트북",
            "description": "고성능 게이밍 노트북",
            "price": 1299.99,
            "tax": 129.99,
            "tags": ["gaming", "laptop", "high-performance"],
            "images": [
                {
                    "url": "https://picsum.photos/800/600",
                    "name": "메인 이미지",
                    "type": "jpeg",
                    "size": 1024000,
                    "alt_text": "노트북 메인 이미지"
                }
            ],
            "category": {
                "id": 1,
                "name": "컴퓨터",
                "parent_id": None
            },
            "metadata": {
                "brand": "TechBrand",
                "model": "TB-2024",
                "warranty": 2
            },
            "status": "published"
        },
        "complex_offer": {
            "name": "게이밍 세트 특가",
            "description": "게이밍을 위한 완벽한 세트 상품",
            "items": [
                {
                    "name": "게이밍 노트북",
                    "price": 1999.99,
                    "tags": ["gaming", "laptop"],
                    "images": [],
                    "metadata": {"type": "main"},
                    "status": "published"
                },
                {
                    "name": "게이밍 마우스",
                    "price": 79.99,
                    "tags": ["gaming", "mouse"],
                    "images": [],
                    "metadata": {"type": "accessory"},
                    "status": "published"
                }
            ],
            "seller": {
                "name": "게이밍샵",
                "company": {
                    "name": "(주)게이밍코리아",
                    "registration_number": "123-45-67890",
                    "address": {
                        "street": "서울특별시 강남구 테헤란로 123",
                        "city": "서울",
                        "postal_code": "06234",
                        "country": "KR"
                    },
                    "contact": {
                        "email": "info@gaming.co.kr",
                        "phone": "02-1234-5678",
                        "website": "https://gaming.co.kr"
                    }
                },
                "personal_contact": {
                    "email": "seller@gaming.co.kr",
                    "phone": "010-1234-5678"
                },
                "verified": True,
                "rating": 4.8
            },
            "discount_percentage": 10,
            "valid_until": "2024-12-31T23:59:59",
            "terms_and_conditions": [
                "30일 무료 반품 가능",
                "1년 무상 A/S 제공",
                "전국 무료배송"
            ]
        },
        "bulk_request": {
            "items": [
                {
                    "name": "상품 1",
                    "price": 99.99,
                    "tags": ["tag1"],
                    "images": [],
                    "metadata": {},
                    "status": "draft"
                },
                {
                    "name": "상품 2", 
                    "price": 149.99,
                    "tags": ["tag2"],
                    "images": [],
                    "metadata": {},
                    "status": "published"
                }
            ],
            "default_category": {
                "id": 10,
                "name": "기본 카테고리"
            },
            "apply_bulk_discount": True
        }
    }