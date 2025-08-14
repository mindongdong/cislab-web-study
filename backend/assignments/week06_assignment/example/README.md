# 📚 도서 관리 시스템 API - Week 06 테스트 스위트

이 프로젝트는 [Week 05 과제](../week05_assignment)에서 구현된 FastAPI 도서 관리 시스템 API에 대한 포괄적인 테스트 스위트를 포함합니다.

## 🎯 프로젝트 목표

- **코드 중복 제거**: Week 05의 API 코드를 직접 참조하여 테스트 환경의 효율성을 높입니다.
- **전문적인 테스트 환경 구축**: `pytest`를 사용하여 실제 운영 환경 수준의 테스트 스위트를 구현합니다.
- **테스트 중심 개발(TDD) 원칙 시연**: 잘 작성된 테스트가 어떻게 API의 안정성과 품질을 보장하는지 보여줍니다.

## 🏗️ 프로젝트 구조

이 디렉토리는 Week 05 API를 테스트하기 위한 파일들로만 구성되어 있습니다. **API 소스 코드는 포함되어 있지 않습니다.**

```
week06_assignment/example/
├── 📄 pytest.ini                    # pytest 설정 파일
├── 📄 requirements-test.txt          # 테스트 실행에 필요한 패키지
├── 📄 TEST_README.md                # 상세 테스트 실행 가이드
├── 📄 TESTING_SUMMARY.md            # 테스트 구현 요약
├── 🐍 run_tests.py                  # 테스트 실행 자동화 스크립트
└── 📁 tests/                        # 💎 Pytest 테스트 스위트
    ├── 🐍 conftest.py               # 공통 Fixture 및 테스트 설정
    ├── 📁 api/
    │   ├── 🧪 test_books.py         # 도서 API 테스트
    │   └── 🧪 test_categories.py    # 카테고리 API 테스트
    ├── 🧪 test_main.py              # 애플리케이션 핵심 동작 테스트
    └── 🧪 test_mocking.py           # 외부 서비스 모킹 테스트
```

## 🧪 테스트 실행

이 테스트 스위트를 실행하여 Week 05 API의 모든 기능이 정상적으로 작동하는지 검증할 수 있습니다.

### 1. 의존성 설치

테스트 실행에 필요한 Python 패키지를 설치합니다. (API 자체의 의존성은 Week 05 디렉토리에 있는 `requirements.txt`를 통해 설치해야 합니다.)

```bash
# 테스트 관련 의존성 설치
pip install -r requirements-test.txt
```

### 2. 테스트 실행

아래 명령어를 사용하여 전체 테스트 스위트를 실행합니다.

```bash
# 1. 간단한 실행
pytest

# 2. 상세 정보와 함께 실행
pytest -v

# 3. 자동화 스크립트 사용 (권장)
python run_tests.py
```

테스트 실행에 대한 더 자세한 옵션과 설명은 [TEST_README.md](./TEST_README.md) 파일을 참고하십시오.

## 🔍 주요 테스트 범위

- **API 엔드포인트**: 모든 CRUD 및 비즈니스 로직 엔드포인트 검증
- **데이터 유효성**: 잘못된 입력값에 대한 에러 처리 검증
- **에러 케이스**: 예외 상황 및 경계값 테스트
- **외부 서비스 연동**: `unittest.mock`을 사용한 외부 API 호출 모킹
- **데이터베이스 트랜잭션**: 테스트 격리 및 데이터 일관성 보장

이 프로젝트는 Week 05의 결과물을 기반으로 한 단계 더 나아가, 견고하고 신뢰성 있는 소프트웨어를 만들기 위한 테스트의 중요성을 보여줍니다.