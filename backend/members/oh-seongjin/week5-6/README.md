## 파일 구조
```text
app  
├─ README.md                  
├─ requirements.txt           
├─ pytest.ini                 # 테스트 실행 옵션
├─ app/  
│  ├─ main.py                 # FastAPI 앱 생성, 라우터 등록, 테이블 생성  
│  ├─ core/  
│  │  └─ config.py            # 설정 로드  
│  ├─ db/  
│  │  ├─ base.py              # SQLAlchemy Base  
│  │  └─ session.py           # 엔진 생성  
│  ├─ models/  
│  │  ├─ __init__.py          
│  │  ├─ book.py              # book ORM  
│  │  └─ category.py          # category ORM  
│  ├─ schemas/  
│  │  ├─ __init__.py          
│  │  ├─ book.py              # book 스키마  
│  │  └─ category.py          # category 스키마  
│  ├─ api/  
│  │  ├─ __init__.py          
│  │  ├─ deps.py              # DB 세션 주입  
│  │  └─ routes/  
│  │     ├─ __init__.py       
│  │     ├─ books.py          # books 엔드포인트  
│  │     └─ categories.py     # categories 엔드포인트  
│  ├─ utils/  
│  │     └─ responses.py      # 응답 형식
│  └─ test/
│  │     ├─ README.md
│        └─ ...               # README.md 참고
```

## 의존성 설치
```bash
pip install -r requirements.txt
```

## 실행
```bash  
uvicorn app.main:app --reload
```