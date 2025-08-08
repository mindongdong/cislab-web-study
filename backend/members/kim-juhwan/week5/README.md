# 5주차 과제

## 1. backend 과제: FastAPI + SQLAlchemy 실습 과제: 도서 관리 시스템 API 구축

 - pdf 파일 첨부


| 계층 (Layer) | 핵심 역할 | 구현 기술 / 파일 |
| :--- | :--- | :--- |
| **① API 계층** | HTTP 요청/응답 처리, 경로 설정 | `FastAPI`, `api/` |
| **② 비즈니스 로직** | 앱 규칙 적용, 데이터 가공, 흐름 제어 | `api/` 및 `repository/` 내 로직 |
| **③ 데이터 접근 계층** | DB 통신 캡슐화 (CRUD) | `Repository Pattern`, `database/repository.py` |
| **④ 데이터베이스** | 데이터 영구 저장 및 관리 | `MySQL`, `database/orm.py` |
| **(별도) 스키마 계층** | 데이터 형식 정의, 유효성 검사 | `Pydantic`, `schema/` |
