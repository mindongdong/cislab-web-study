1. connection.py
-database와 연결하고, get_db메서드 생성

(1)created_engine을 통해 database url연결
(2)sessionmaker를 통해 engine binding, sessionFacTory생성
(3) get_db : session객체가 생성되고, 다시 닫히는 메서드 생성

2. orm.py
 - declarative_base -> 테이블 객체를 생성한다.

(1) Book
(2) Category

3. DTO.py
- reponse와 request의 유효성 검사를 실시하기 위한 모델 생성

(1) BookModel
(2) CategoryModel
(3) ListBookModel : main.py에서 List[BookModel]로 대체.

4. service.py
- 로직 처리과 예외처리
(1) 전체 도서목록 리스트 조회-페이징, 상세검색 등의 쿼리파라미터 포함
(2) id로 도서목록 조회
(3) 전체 카테고리 목록 리스트 조회
(4) 새 도서 등록 -isbn 중복 확인후 resposne
(5) 새 카테고리 등록 -name_exist로 중복 검사후 response
(6) 도서 정보 수정 -book_exist로 실제 존재 확인후 resposne
(7) 도서 삭제
(8) 재고관리 - quantity와 operation 변수

5.main.py : api계층
-request와 response만을 담당한다.
-service.py의 함수를 호출하고, results에 담고, 바로 반환한다.
-모든 로직을 service에서 처리하고, api계층은 최소화 한다.

###
┌───────────────────────────┐
│         CPU Cache         │ ← 하드웨어 (SQLAlchemy와 무관)
└───────────────────────────┘
┌───────────────────────────┐
│         RAM(메인메모리)    │
│  ┌───────────────────────┐ │
│  │ Python 프로세스 Heap  │ │
│  │   ┌─────────────────┐ │ │
│  │   │ SQLAlchemy      │ │ │
│  │   │ Session 객체    │ │ │
│  │   │  (Identity Map) │ │ │ ← SQLAlchemy 1차 캐시
│  │   └─────────────────┘ │ │
│  └───────────────────────┘ │
└───────────────────────────┘
*** Session 객체가 관리하는 딕셔너리 형태:
key = ORM 클래스, PK
value = ORM 객체 인스턴스
{Book : books}