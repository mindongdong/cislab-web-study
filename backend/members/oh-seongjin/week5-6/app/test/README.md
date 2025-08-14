## 파일 구조
test
├─ README.md  
└─ test.py         # 테스트

## 의존성 설치
```bash
pip install -r requirements.txt
```

## 실행
```bash
pytest # 실행
pytest --cov=app --cov-report=html # 리포트 생성
```