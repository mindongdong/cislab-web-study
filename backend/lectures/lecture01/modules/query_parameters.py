"""
쿼리 매개변수 (Query Parameters) 학습 모듈

강의 내용:
1. 기본 쿼리 매개변수 사용법
2. 기본값과 선택적 매개변수
3. 타입 변환 (bool, int, float 등)
4. 필수 쿼리 매개변수
5. 쿼리 매개변수 리스트/다중 값
6. Query를 사용한 고급 검증
"""

from typing import List, Optional, Union
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from enum import Enum

# 라우터 생성
router = APIRouter()

# Enum 정의
class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

# 응답 모델 정의
class SearchResult(BaseModel):
    query: str
    results: List[str]
    total_count: int
    page: int
    limit: int

class User(BaseModel):
    id: int
    name: str
    email: str
    role: str
    active: bool
    created_at: str

class PaginatedResponse(BaseModel):
    items: List[User]
    total: int
    page: int
    size: int
    pages: int

# 1. 기본 쿼리 매개변수 예제

@router.get("/")
async def query_root():
    """쿼리 매개변수 모듈의 루트"""
    return {
        "message": "쿼리 매개변수 학습 모듈",
        "available_endpoints": [
            "/search?q=검색어 - 기본 검색",
            "/items?skip=0&limit=10 - 페이지네이션",
            "/users?active=true&role=admin - 필터링",
            "/products?tags=tag1,tag2 - 리스트 매개변수",
            "/advanced?required_param=value - 고급 검증"
        ]
    }

@router.get("/search")
async def search_items(
    q: str,  # 필수 쿼리 매개변수 (기본값 없음)
    page: int = 1,  # 선택적 매개변수 (기본값 있음)
    limit: int = 10,  # 선택적 매개변수
    sort: SortOrder = SortOrder.asc  # Enum 기본값
):
    """
    기본 검색 API
    - q: 검색어 (필수)
    - page: 페이지 번호 (기본값: 1)
    - limit: 페이지당 결과 수 (기본값: 10)
    - sort: 정렬 순서 (기본값: asc)
    """
    if not q.strip():
        raise HTTPException(status_code=400, detail="검색어는 비어있을 수 없습니다")
    
    if page < 1:
        raise HTTPException(status_code=400, detail="페이지 번호는 1 이상이어야 합니다")
    
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit은 1-100 사이여야 합니다")
    
    # 가짜 검색 결과 생성
    all_results = [
        f"{q} 관련 결과 {i}" for i in range(1, 51)
    ]
    
    # 정렬 적용
    if sort == SortOrder.desc:
        all_results.reverse()
    
    # 페이지네이션 적용
    start = (page - 1) * limit
    end = start + limit
    page_results = all_results[start:end]
    
    return SearchResult(
        query=q,
        results=page_results,
        total_count=len(all_results),
        page=page,
        limit=limit
    )

# 2. 선택적 매개변수와 Union 타입

@router.get("/items")
async def get_items(
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,  # 선택적 문자열
    min_price: Optional[float] = None,  # 선택적 실수
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None  # 선택적 불린
):
    """
    상품 목록 조회 API
    - skip: 건너뛸 항목 수
    - limit: 가져올 항목 수  
    - category: 카테고리 필터 (선택적)
    - min_price, max_price: 가격 범위 (선택적)
    - in_stock: 재고 여부 (선택적)
    """
    # 가짜 상품 데이터
    all_items = [
        {"id": i, "name": f"상품 {i}", "category": "electronics" if i % 2 == 0 else "clothing", 
         "price": 10.0 + (i * 5.5), "in_stock": i % 3 != 0}
        for i in range(1, 101)
    ]
    
    # 필터 적용
    filtered_items = all_items
    
    if category:
        filtered_items = [item for item in filtered_items if item["category"] == category]
    
    if min_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] >= min_price]
    
    if max_price is not None:
        filtered_items = [item for item in filtered_items if item["price"] <= max_price]
    
    if in_stock is not None:
        filtered_items = [item for item in filtered_items if item["in_stock"] == in_stock]
    
    # 페이지네이션 적용
    total = len(filtered_items)
    items = filtered_items[skip:skip + limit]
    
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
        "filters_applied": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock
        }
    }

# 3. bool 타입 자동 변환

@router.get("/users")
async def get_users(
    active: bool = True,  # bool 타입 자동 변환
    role: Optional[UserRole] = None,
    page: int = 1,
    size: int = 20
):
    """
    사용자 목록 조회 API
    - active: 활성 사용자만 조회 (true/false, 1/0, yes/no 등 자동 변환)
    - role: 사용자 역할 필터
    - page: 페이지 번호
    - size: 페이지 크기
    """
    # 가짜 사용자 데이터 생성
    all_users = []
    for i in range(1, 101):
        user_roles = ["admin", "user", "guest"]
        all_users.append(User(
            id=i,
            name=f"사용자{i}",
            email=f"user{i}@example.com",
            role=user_roles[i % 3],
            active=i % 4 != 0,  # 75% 활성
            created_at=f"2024-01-{(i % 28) + 1:02d}T00:00:00"
        ))
    
    # 필터 적용
    filtered_users = [user for user in all_users if user.active == active]
    
    if role:
        filtered_users = [user for user in filtered_users if user.role == role.value]
    
    # 페이지네이션
    total = len(filtered_users)
    start = (page - 1) * size
    end = start + size
    users = filtered_users[start:end]
    
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size  # 올림 계산
    )

# 4. 필수 쿼리 매개변수 (Query(...) 사용)

@router.get("/reports")
async def generate_report(
    start_date: str = Query(..., description="시작 날짜 (YYYY-MM-DD)"),
    end_date: str = Query(..., description="종료 날짜 (YYYY-MM-DD)"),
    report_type: str = Query(..., pattern="^(daily|weekly|monthly)$", description="리포트 타입"),
    email: Optional[str] = Query(None, pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", 
                                description="결과를 받을 이메일 (선택적)")
):
    """
    리포트 생성 API
    - start_date, end_date: 필수 날짜 매개변수
    - report_type: 정규식으로 검증되는 필수 매개변수
    - email: 정규식으로 검증되는 선택적 매개변수
    """
    from datetime import datetime
    
    try:
        # 날짜 형식 검증
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        
        if start > end:
            raise HTTPException(status_code=400, detail="시작 날짜가 종료 날짜보다 늦을 수 없습니다")
        
    except ValueError:
        raise HTTPException(status_code=400, detail="날짜 형식이 올바르지 않습니다 (YYYY-MM-DD)")
    
    # 리포트 생성 시뮬레이션
    report_data = {
        "report_id": f"RPT_{start_date}_{end_date}_{report_type}",
        "parameters": {
            "start_date": start_date,
            "end_date": end_date,
            "report_type": report_type,
            "email": email
        },
        "status": "generated",
        "generated_at": datetime.now().isoformat(),
        "data": {
            "total_records": 1250,
            "summary": f"{report_type} 리포트 ({start_date} ~ {end_date})",
            "charts": ["sales_trend", "user_activity", "revenue_breakdown"]
        }
    }
    
    if email:
        report_data["delivery"] = {
            "method": "email",
            "recipient": email,
            "sent": True
        }
    
    return report_data

# 5. 쿼리 매개변수 리스트/다중 값

@router.get("/products")
async def get_products(
    tags: List[str] = Query(default=[], description="상품 태그 목록"),
    categories: List[str] = Query(default=["all"], description="카테고리 목록"),
    ids: Optional[List[int]] = Query(default=None, description="특정 상품 ID 목록")
):
    """
    상품 조회 API (리스트 매개변수 사용)
    - tags: 여러 태그로 필터링 (?tags=tag1&tags=tag2 또는 ?tags=tag1,tag2)
    - categories: 여러 카테고리로 필터링
    - ids: 특정 ID 목록으로 조회
    
    사용 예시:
    - /products?tags=electronics&tags=sale&categories=laptop&categories=phone
    - /products?ids=1&ids=2&ids=3
    """
    # 가짜 상품 데이터
    all_products = []
    for i in range(1, 51):
        product_tags = []
        if i % 2 == 0:
            product_tags.append("electronics")
        if i % 3 == 0:
            product_tags.append("sale")
        if i % 5 == 0:
            product_tags.append("featured")
        if i % 7 == 0:
            product_tags.append("new")
            
        product_categories = ["laptop" if i % 4 == 0 else "phone" if i % 4 == 1 else "tablet" if i % 4 == 2 else "accessory"]
        
        all_products.append({
            "id": i,
            "name": f"상품 {i}",
            "tags": product_tags,
            "categories": product_categories,
            "price": 50.0 + (i * 10.5)
        })
    
    filtered_products = all_products
    
    # ID 필터 (가장 우선)
    if ids:
        filtered_products = [p for p in filtered_products if p["id"] in ids]
    
    # 태그 필터
    if tags:
        filtered_products = [
            p for p in filtered_products 
            if any(tag in p["tags"] for tag in tags)
        ]
    
    # 카테고리 필터 ("all"이 아닌 경우에만)
    if categories and "all" not in categories:
        filtered_products = [
            p for p in filtered_products 
            if any(cat in p["categories"] for cat in categories)
        ]
    
    return {
        "products": filtered_products,
        "total_found": len(filtered_products),
        "filters_applied": {
            "tags": tags,
            "categories": categories,
            "ids": ids
        },
        "available_filters": {
            "all_tags": ["electronics", "sale", "featured", "new"],
            "all_categories": ["laptop", "phone", "tablet", "accessory"]
        }
    }

# 6. Query를 사용한 고급 검증

@router.get("/advanced")
async def advanced_query_validation(
    required_param: str = Query(..., min_length=3, max_length=50, 
                               description="필수 매개변수 (3-50자)"),
    numeric_param: int = Query(default=1, ge=1, le=100, 
                              description="숫자 매개변수 (1-100)"),
    float_param: float = Query(default=0.0, gt=0.0, lt=1000.0,
                              description="실수 매개변수 (0초과 1000미만)"),
    regex_param: Optional[str] = Query(default=None, pattern="^[A-Z]{2,5}$",
                                      description="정규식 매개변수 (대문자 2-5자)"),
    deprecated_param: Optional[str] = Query(default=None, deprecated=True,
                                           description="더 이상 사용되지 않는 매개변수")
):
    """
    고급 쿼리 매개변수 검증 예제
    - 문자열 길이 제한
    - 숫자 범위 제한  
    - 정규식 검증
    - 매개변수 deprecation
    """
    result = {
        "required_param": required_param,
        "numeric_param": numeric_param,
        "float_param": float_param,
        "validation_passed": True,
        "metadata": {
            "required_length": len(required_param),
            "numeric_squared": numeric_param ** 2,
            "float_percentage": f"{float_param:.2%}"
        }
    }
    
    if regex_param:
        result["regex_param"] = regex_param
        result["regex_validation"] = "정규식 검증 통과"
    
    if deprecated_param:
        result["deprecated_param"] = deprecated_param
        result["warning"] = "deprecated_param은 더 이상 사용되지 않습니다"
    
    return result

# 7. 복합 쿼리 매개변수 예제

@router.get("/analytics")
async def get_analytics(
    metrics: List[str] = Query(default=["views", "clicks"], 
                              description="분석할 지표들"),
    start_date: Optional[str] = Query(default=None, 
                                     description="시작 날짜 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(default=None,
                                   description="종료 날짜 (YYYY-MM-DD)"),
    granularity: str = Query(default="daily", pattern="^(hourly|daily|weekly|monthly)$",
                            description="데이터 세분화 수준"),
    include_meta: bool = Query(default=False, description="메타데이터 포함 여부"),
    export_format: Optional[str] = Query(default=None, pattern="^(json|csv|xlsx)$",
                                        description="내보내기 형식")
):
    """
    복합 분석 데이터 조회 API
    다양한 타입의 쿼리 매개변수를 조합한 실제 사용 사례
    """
    from datetime import datetime, timedelta
    
    # 기본 날짜 설정 (설정되지 않은 경우)
    if not start_date:
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    # 가짜 분석 데이터 생성
    analytics_data = {
        "query_parameters": {
            "metrics": metrics,
            "date_range": {"start": start_date, "end": end_date},
            "granularity": granularity,
            "export_format": export_format
        },
        "data": {}
    }
    
    # 지표별 데이터 생성
    for metric in metrics:
        if metric == "views":
            analytics_data["data"]["views"] = {"total": 15420, "average_daily": 2203}
        elif metric == "clicks":
            analytics_data["data"]["clicks"] = {"total": 1250, "average_daily": 178}
        elif metric == "conversions":
            analytics_data["data"]["conversions"] = {"total": 89, "rate": 7.12}
        else:
            analytics_data["data"][metric] = {"total": 0, "note": "지원되지 않는 지표"}
    
    # 메타데이터 포함
    if include_meta:
        analytics_data["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "data_source": "analytics_db",
            "confidence_level": 95.5,
            "sample_size": 10000
        }
    
    # 내보내기 정보
    if export_format:
        analytics_data["export"] = {
            "format": export_format,
            "download_url": f"/exports/{export_format}/analytics_{start_date}_{end_date}",
            "estimated_size": "2.5MB" if export_format == "xlsx" else "1.2MB"
        }
    
    return analytics_data