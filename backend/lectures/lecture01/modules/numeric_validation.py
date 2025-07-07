"""
숫자 검증 (Numeric Validation) 학습 모듈

강의 내용:
1. Path 및 Query를 사용한 숫자 검증
2. 메타데이터 선언 (title, description)
3. 매개변수 정렬과 키워드 인자 트릭
4. 숫자 검증 키워드 (ge, gt, le, lt)
5. float 값에 대한 검증
6. 복합 검증 시나리오
"""

from typing import Optional
from fastapi import APIRouter, Path, Query, HTTPException
from pydantic import BaseModel, Field
from enum import Enum

# 라우터 생성
router = APIRouter()

# 응답 모델 정의
class ItemDetail(BaseModel):
    """상품 상세 정보 모델"""
    item_id: int
    name: str
    price: float
    rating: Optional[float]
    stock: int
    category: str
    validation_info: dict

class SearchResult(BaseModel):
    """검색 결과 모델"""
    query: str
    page: int
    size: int
    price_range: dict
    rating_filter: Optional[float]
    results: list
    total_count: int

class RangeStats(BaseModel):
    """범위 통계 모델"""
    min_value: float
    max_value: float
    average: float
    count: int
    valid_range: dict

# 1. 기본 숫자 검증

@router.get("/")
async def validation_root():
    """숫자 검증 모듈의 루트"""
    return {
        "message": "숫자 검증 학습 모듈",
        "available_endpoints": [
            "/items/{item_id} - Path 숫자 검증",
            "/search - Query 숫자 검증", 
            "/products/{product_id} - 복합 검증",
            "/range-stats - 범위 통계",
            "/advanced-filter - 고급 필터링"
        ],
        "validation_keywords": {
            "ge": "크거나 같음 (>=)",
            "gt": "큼 (>)",
            "le": "작거나 같음 (<=)",
            "lt": "작음 (<)"
        }
    }

@router.get("/items/{item_id}", response_model=ItemDetail)
async def get_item_with_validation(
    item_id: int = Path(
        ...,
        title="상품 ID",
        description="조회할 상품의 고유 식별자",
        ge=1,
        le=1000,
        example=42
    ),
    rating: Optional[float] = Query(
        None,
        title="평점 필터",
        description="최소 평점 (0.0 이상 5.0 이하)",
        ge=0.0,
        le=5.0,
        example=4.0
    )
):
    """
    상품 상세 조회 API (기본 숫자 검증)
    - item_id: 1 이상 1000 이하의 정수
    - rating: 0.0 이상 5.0 이하의 실수 (선택적)
    """
    # 상품 존재 여부 확인 시뮬레이션
    if item_id > 500:  # 500번 이후는 존재하지 않는다고 가정
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    
    # 가짜 상품 데이터 생성
    categories = ["electronics", "clothing", "books", "home", "sports"]
    category = categories[item_id % len(categories)]
    
    item_rating = 3.5 + (item_id % 10) * 0.15  # 3.5 ~ 4.85 범위
    
    # 평점 필터 적용
    if rating and item_rating < rating:
        raise HTTPException(
            status_code=404, 
            detail=f"평점 {rating} 이상의 조건을 만족하는 상품이 아닙니다 (현재 평점: {item_rating:.1f})"
        )
    
    return ItemDetail(
        item_id=item_id,
        name=f"상품 {item_id}",
        price=10.0 + (item_id * 5.99),
        rating=round(item_rating, 1),
        stock=100 - (item_id % 50),
        category=category,
        validation_info={
            "item_id_range": "1-1000",
            "rating_range": "0.0-5.0",
            "rating_filter_applied": rating is not None,
            "passed_validations": ["path_range", "query_range"]
        }
    )

# 2. 복잡한 쿼리 매개변수 검증

@router.get("/search", response_model=SearchResult)
async def search_products(
    q: str = Query(..., min_length=1, max_length=100, description="검색어"),
    page: int = Query(
        1,
        title="페이지 번호",
        description="조회할 페이지 번호 (1부터 시작)",
        ge=1,
        le=1000,
        example=1
    ),
    size: int = Query(
        10,
        title="페이지 크기",
        description="한 페이지당 결과 수",
        ge=1,
        le=100,
        example=10
    ),
    min_price: Optional[float] = Query(
        None,
        title="최소 가격",
        description="최소 가격 필터 (0 이상)",
        ge=0.0,
        example=10.0
    ),
    max_price: Optional[float] = Query(
        None,
        title="최대 가격",
        description="최대 가격 필터 (최소 가격보다 큰 값)",
        gt=0.0,
        le=100000.0,
        example=1000.0
    ),
    min_rating: Optional[float] = Query(
        None,
        title="최소 평점",
        description="최소 평점 필터",
        ge=0.0,
        le=5.0,
        example=4.0
    )
):
    """
    상품 검색 API (복합 숫자 검증)
    - 페이지네이션 검증
    - 가격 범위 검증
    - 평점 필터 검증
    """
    # 가격 범위 논리 검증
    if min_price and max_price and min_price >= max_price:
        raise HTTPException(
            status_code=400,
            detail="최소 가격은 최대 가격보다 작아야 합니다"
        )
    
    # 가짜 검색 결과 생성
    total_products = 500
    
    # 필터 적용 시뮬레이션
    filtered_count = total_products
    if min_price:
        filtered_count = int(filtered_count * 0.7)  # 30% 필터링
    if max_price:
        filtered_count = int(filtered_count * 0.8)  # 20% 필터링
    if min_rating:
        filtered_count = int(filtered_count * 0.6)  # 40% 필터링
    
    # 페이지 범위 검증
    max_pages = (filtered_count + size - 1) // size
    if page > max_pages:
        raise HTTPException(
            status_code=400,
            detail=f"페이지 번호가 범위를 초과했습니다 (최대: {max_pages})"
        )
    
    # 결과 생성
    start_idx = (page - 1) * size
    results = []
    for i in range(size):
        product_id = start_idx + i + 1
        if product_id <= filtered_count:
            results.append({
                "id": product_id,
                "name": f"{q} 관련 상품 {product_id}",
                "price": 50.0 + (product_id * 2.5),
                "rating": 3.0 + (product_id % 20) * 0.1
            })
    
    return SearchResult(
        query=q,
        page=page,
        size=size,
        price_range={
            "min": min_price,
            "max": max_price,
            "applied": min_price is not None or max_price is not None
        },
        rating_filter=min_rating,
        results=results,
        total_count=filtered_count
    )

# 3. 키워드 인자 트릭 (*를 사용한 매개변수 정렬)

@router.get("/products/{product_id}")
async def get_product_advanced(
    *,  # 이후 모든 매개변수는 키워드 인자만 허용
    product_id: int = Path(
        ...,
        title="상품 ID",
        description="상품 식별자",
        ge=1,
        lt=10000
    ),
    version: int = Query(
        1,
        title="API 버전",
        description="API 버전 번호",
        ge=1,
        le=3
    ),
    include_reviews: bool = Query(
        False,
        title="리뷰 포함",
        description="리뷰 정보 포함 여부"
    ),
    review_limit: int = Query(
        5,
        title="리뷰 개수",
        description="포함할 리뷰 개수",
        ge=1,
        le=50
    )
):
    """
    고급 상품 조회 API
    - * 를 사용하여 모든 매개변수를 키워드 인자로 강제
    - 매개변수 순서에 관계없이 명확한 API 사용 가능
    """
    # 상품 기본 정보
    product_info = {
        "id": product_id,
        "name": f"고급 상품 {product_id}",
        "price": 100.0 + (product_id * 10.5),
        "api_version": version,
        "generated_at": "2024-01-15T10:30:00"
    }
    
    # 리뷰 정보 포함
    if include_reviews:
        reviews = []
        for i in range(min(review_limit, 10)):  # 최대 10개까지만
            reviews.append({
                "id": i + 1,
                "rating": 3.0 + (i % 5),
                "comment": f"리뷰 {i + 1}",
                "author": f"사용자{i + 1}"
            })
        
        product_info["reviews"] = reviews
        product_info["review_summary"] = {
            "total_shown": len(reviews),
            "average_rating": sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
        }
    
    return product_info

# 4. 범위 통계 API

@router.get("/range-stats", response_model=RangeStats)
async def get_range_statistics(
    min_value: float = Query(
        0.0,
        title="최솟값",
        description="통계 계산할 최솟값",
        ge=0.0
    ),
    max_value: float = Query(
        100.0,
        title="최댓값", 
        description="통계 계산할 최댓값",
        gt=0.0,
        le=10000.0
    ),
    sample_size: int = Query(
        100,
        title="샘플 크기",
        description="생성할 샘플 데이터 크기",
        ge=10,
        le=1000
    )
):
    """
    범위 통계 계산 API
    - 실수 범위 검증
    - 논리적 범위 검증 (min < max)
    - 통계 계산 시뮬레이션
    """
    # 범위 논리 검증
    if min_value >= max_value:
        raise HTTPException(
            status_code=400,
            detail="최솟값은 최댓값보다 작아야 합니다"
        )
    
    # 가짜 통계 계산
    import random
    random.seed(42)  # 일관된 결과를 위한 시드 설정
    
    samples = [
        random.uniform(min_value, max_value) 
        for _ in range(sample_size)
    ]
    
    average = sum(samples) / len(samples)
    
    return RangeStats(
        min_value=min_value,
        max_value=max_value,
        average=round(average, 2),
        count=sample_size,
        valid_range={
            "provided_min": min_value,
            "provided_max": max_value,
            "range_size": max_value - min_value,
            "sample_count": sample_size
        }
    )

# 5. 고급 필터링 API

@router.get("/advanced-filter")
async def advanced_numeric_filter(
    # 정수 필터들
    category_id: Optional[int] = Query(
        None,
        title="카테고리 ID",
        description="필터링할 카테고리 ID",
        ge=1,
        le=100
    ),
    stock_min: int = Query(
        0,
        title="최소 재고",
        description="최소 재고 수량",
        ge=0
    ),
    # 실수 필터들
    price_min: float = Query(
        0.0,
        title="최소 가격",
        description="최소 가격 (0 이상)",
        ge=0.0
    ),
    price_max: float = Query(
        1000000.0,
        title="최대 가격",
        description="최대 가격 (최소 가격보다 큰 값)",
        gt=0.0,
        le=1000000.0
    ),
    discount_min: Optional[float] = Query(
        None,
        title="최소 할인율",
        description="최소 할인율 (0% 이상 100% 미만)",
        ge=0.0,
        lt=100.0
    ),
    rating_exact: Optional[float] = Query(
        None,
        title="정확한 평점",
        description="정확히 일치하는 평점 (0.0-5.0)",
        ge=0.0,
        le=5.0
    ),
    # 범위 제한
    limit: int = Query(
        20,
        title="결과 개수",
        description="반환할 결과 개수",
        ge=1,
        le=100
    )
):
    """
    고급 숫자 필터링 API
    - 다양한 숫자 타입 검증 조합
    - 논리적 범위 검증
    - 복합 필터 조건
    """
    # 가격 범위 검증
    if price_min >= price_max:
        raise HTTPException(
            status_code=400,
            detail="최소 가격은 최대 가격보다 작아야 합니다"
        )
    
    # 필터 조건 정리
    active_filters = {}
    if category_id:
        active_filters["category_id"] = category_id
    if stock_min > 0:
        active_filters["stock_min"] = stock_min
    if price_min > 0:
        active_filters["price_min"] = price_min
    if price_max < 1000000:
        active_filters["price_max"] = price_max
    if discount_min:
        active_filters["discount_min"] = discount_min
    if rating_exact:
        active_filters["rating_exact"] = rating_exact
    
    # 가짜 필터링 결과 생성
    base_count = 1000
    filtered_count = base_count
    
    # 각 필터별 감소율 적용
    if category_id:
        filtered_count = int(filtered_count * 0.3)  # 카테고리 필터링 시 70% 감소
    if stock_min > 0:
        filtered_count = int(filtered_count * 0.8)  # 재고 필터링 시 20% 감소
    if price_min > 0 or price_max < 1000000:
        filtered_count = int(filtered_count * 0.6)  # 가격 필터링 시 40% 감소
    if discount_min:
        filtered_count = int(filtered_count * 0.4)  # 할인 필터링 시 60% 감소
    if rating_exact:
        filtered_count = int(filtered_count * 0.1)  # 정확한 평점 시 90% 감소
    
    # 결과 생성
    results = []
    for i in range(min(limit, filtered_count)):
        product = {
            "id": i + 1,
            "name": f"필터된 상품 {i + 1}",
            "category_id": category_id or (i % 10) + 1,
            "stock": stock_min + (i % 50),
            "price": max(price_min, 50.0 + (i * 12.5)),
            "discount": discount_min or (i % 50),
            "rating": rating_exact or round(3.0 + (i % 20) * 0.1, 1)
        }
        
        # 가격 범위 체크
        if product["price"] <= price_max:
            results.append(product)
    
    return {
        "results": results[:limit],
        "total_filtered": filtered_count,
        "active_filters": active_filters,
        "filter_summary": {
            "original_count": base_count,
            "filtered_count": filtered_count,
            "reduction_percentage": round((1 - filtered_count / base_count) * 100, 1),
            "returned_count": len(results[:limit])
        },
        "validation_passed": {
            "price_range_valid": price_min < price_max,
            "all_numeric_ranges_valid": True,
            "filter_count": len(active_filters)
        }
    }