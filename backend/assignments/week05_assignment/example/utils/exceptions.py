"""
커스텀 예외 클래스 정의
- 비즈니스 로직에서 발생하는 예외를 체계적으로 관리
"""
from typing import Optional

class BusinessException(Exception):
    """비즈니스 로직 예외 기본 클래스"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(BusinessException):
    """리소스를 찾을 수 없을 때 발생하는 예외"""
    def __init__(self, resource: str, id: Optional[int] = None):
        message = f"{resource}을(를) 찾을 수 없습니다"
        if id:
            message = f"{resource} (ID: {id})을(를) 찾을 수 없습니다"
        super().__init__(message, 404)

class DuplicateException(BusinessException):
    """중복된 데이터가 있을 때 발생하는 예외"""
    def __init__(self, field: str, value: str):
        message = f"이미 존재하는 {field}입니다: {value}"
        super().__init__(message, 409)

class InsufficientStockException(BusinessException):
    """재고가 부족할 때 발생하는 예외"""
    def __init__(self, current_stock: int, requested: int):
        message = f"재고가 부족합니다. 현재 재고: {current_stock}, 요청 수량: {requested}"
        super().__init__(message, 400)

class InvalidOperationException(BusinessException):
    """유효하지 않은 작업을 시도할 때 발생하는 예외"""
    def __init__(self, message: str):
        super().__init__(message, 400)