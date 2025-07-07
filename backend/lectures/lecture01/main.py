"""
FastAPI 학습을 위한 메인 서버 파일
강의 내용에 따라 모듈별로 나누어진 API 엔드포인트들을 통합하여 제공합니다.

실행 방법:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

또는:
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

브라우저에서 확인:
- API 문서: http://localhost:8000/docs (Swagger UI)
- 대체 문서: http://localhost:8000/redoc (ReDoc)
- 클라이언트 테스트: http://localhost:8000/client
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# 각 개념별 모듈 import
from modules import path_parameters
from modules import query_parameters  
from modules import request_body
from modules import nested_models
from modules import numeric_validation

# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="FastAPI 학습 API",
    description="백엔드 웹 개발 입문자를 위한 FastAPI 실습 서버",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI 경로
    redoc_url="/redoc"  # ReDoc 경로
)

# 정적 파일 서빙 (CSS, JS 등)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# 1. 기본 Hello World 엔드포인트
@app.get("/")
async def root():
    """
    기본 루트 엔드포인트
    FastAPI 서버가 정상적으로 동작하는지 확인
    """
    return {
        "message": "안녕하세요! FastAPI 학습 서버입니다.", 
        "welcome": "Welcome to FastAPI Learning Server!",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc", 
            "client": "/client",
            "examples": {
                "path_params": "/items/42",
                "query_params": "/search?q=python&limit=10",
                "request_body": "/users/ (POST)",
                "nested_models": "/offers/ (POST)"
            }
        }
    }

@app.get("/hello")
async def hello_world():
    """간단한 Hello World 응답"""
    return {"message": "Hello, World!", "framework": "FastAPI"}

@app.get("/health")
async def health_check():
    """서버 상태 확인용 헬스체크 엔드포인트"""
    return {"status": "healthy", "service": "FastAPI Learning Server"}

# 2. 각 모듈의 라우터 포함
# 경로 매개변수 관련 API
app.include_router(
    path_parameters.router,
    prefix="/path",
    tags=["경로 매개변수 (Path Parameters)"]
)

# 쿼리 매개변수 관련 API  
app.include_router(
    query_parameters.router,
    prefix="/query", 
    tags=["쿼리 매개변수 (Query Parameters)"]
)

# 요청 본문 관련 API
app.include_router(
    request_body.router,
    prefix="/body",
    tags=["요청 본문 (Request Body)"]
)

# 중첩 모델 관련 API
app.include_router(
    nested_models.router,
    prefix="/nested",
    tags=["중첩 모델 (Nested Models)"]
)

# 숫자 검증 관련 API
app.include_router(
    numeric_validation.router,
    prefix="/validation",
    tags=["숫자 검증 (Numeric Validation)"]
)

# 3. 클라이언트 테스트 페이지 제공
@app.get("/client", response_class=HTMLResponse)
async def get_client():
    """
    API 테스트를 위한 간단한 HTML 클라이언트 제공
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI 학습 클라이언트</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 20px;
                line-height: 1.6;
            }
            .container { 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 20px; 
            }
            .section { 
                border: 1px solid #ddd; 
                padding: 20px; 
                border-radius: 8px;
                background-color: #f9f9f9;
            }
            .section h3 { 
                margin-top: 0; 
                color: #333;
                border-bottom: 2px solid #007bff;
                padding-bottom: 10px;
            }
            button { 
                background-color: #007bff; 
                color: white; 
                border: none; 
                padding: 10px 15px; 
                border-radius: 4px; 
                cursor: pointer;
                margin: 5px;
                font-size: 14px;
            }
            button:hover { 
                background-color: #0056b3; 
            }
            input, select, textarea { 
                width: 100%; 
                padding: 8px; 
                margin: 5px 0; 
                border: 1px solid #ddd; 
                border-radius: 4px;
                box-sizing: border-box;
            }
            .result { 
                background-color: #f8f9fa; 
                border: 1px solid #dee2e6; 
                padding: 15px; 
                border-radius: 4px; 
                margin-top: 10px;
                white-space: pre-wrap;
                font-family: monospace;
                max-height: 300px;
                overflow-y: auto;
            }
            .error { 
                background-color: #f8d7da; 
                border-color: #f5c6cb; 
                color: #721c24;
            }
            .success { 
                background-color: #d4edda; 
                border-color: #c3e6cb; 
                color: #155724;
            }
            .api-info {
                background-color: #e7f3ff;
                border: 1px solid #b6d7ff;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .full-width {
                grid-column: 1 / -1;
            }
        </style>
    </head>
    <body>
        <h1>🚀 FastAPI 학습 클라이언트</h1>
        
        <div class="api-info">
            <h3>📚 API 문서 링크</h3>
            <p>
                <a href="/docs" target="_blank">📖 Swagger UI 문서</a> | 
                <a href="/redoc" target="_blank">📘 ReDoc 문서</a>
            </p>
            <p>이 페이지에서 다양한 FastAPI 기능들을 직접 테스트해볼 수 있습니다.</p>
        </div>
        
        <div class="container">
            <!-- 경로 매개변수 테스트 -->
            <div class="section">
                <h3>🛣️ 경로 매개변수 (Path Parameters)</h3>
                <div>
                    <label>Item ID:</label>
                    <input type="number" id="itemId" value="42" placeholder="아이템 ID 입력">
                    <button onclick="testPathParams()">아이템 조회</button>
                </div>
                <div>
                    <label>파일 경로:</label>
                    <input type="text" id="filePath" value="docs/example.txt" placeholder="파일 경로 입력">
                    <button onclick="testFilePath()">파일 조회</button>
                </div>
                <div class="result" id="pathResult">결과가 여기에 표시됩니다.</div>
            </div>

            <!-- 쿼리 매개변수 테스트 -->
            <div class="section">
                <h3>🔍 쿼리 매개변수 (Query Parameters)</h3>
                <div>
                    <label>검색어:</label>
                    <input type="text" id="searchQuery" value="FastAPI" placeholder="검색어 입력">
                    <label>개수 제한:</label>
                    <input type="number" id="limitQuery" value="10" placeholder="결과 개수">
                    <button onclick="testQueryParams()">검색</button>
                </div>
                <div>
                    <label>사용자 필터:</label>
                    <input type="text" id="userFilter" value="admin" placeholder="사용자 타입">
                    <label>활성 여부:</label>
                    <select id="activeFilter">
                        <option value="true">활성</option>
                        <option value="false">비활성</option>
                    </select>
                    <button onclick="testUserFilter()">사용자 필터</button>
                </div>
                <div class="result" id="queryResult">결과가 여기에 표시됩니다.</div>
            </div>

            <!-- 요청 본문 테스트 -->
            <div class="section">
                <h3>📝 요청 본문 (Request Body)</h3>
                <div>
                    <label>사용자 이름:</label>
                    <input type="text" id="userName" value="홍길동" placeholder="이름 입력">
                    <label>이메일:</label>
                    <input type="email" id="userEmail" value="hong@example.com" placeholder="이메일 입력">
                    <label>나이:</label>
                    <input type="number" id="userAge" value="30" placeholder="나이 입력">
                    <button onclick="testCreateUser()">사용자 생성</button>
                </div>
                <div class="result" id="bodyResult">결과가 여기에 표시됩니다.</div>
            </div>

            <!-- 중첩 모델 테스트 -->
            <div class="section">
                <h3>🏗️ 중첩 모델 (Nested Models)</h3>
                <div>
                    <textarea id="offerData" rows="8" placeholder="JSON 데이터 입력">{
  "name": "특별 할인 상품",
  "description": "한정된 시간 동안 제공되는 특별 할인",
  "price": 99.99,
  "items": [
    {
      "name": "노트북",
      "description": "고성능 노트북",
      "price": 1299.99,
      "tags": ["전자제품", "노트북", "고성능"]
    },
    {
      "name": "마우스", 
      "description": "무선 마우스",
      "price": 29.99,
      "tags": ["전자제품", "마우스", "무선"]
    }
  ]
}</textarea>
                    <button onclick="testNestedModel()">상품 등록</button>
                </div>
                <div class="result" id="nestedResult">결과가 여기에 표시됩니다.</div>
            </div>

            <!-- 숫자 검증 테스트 -->
            <div class="section">
                <h3>🔢 숫자 검증 (Numeric Validation)</h3>
                <div>
                    <label>상품 ID (1-1000):</label>
                    <input type="number" id="validationId" value="100" min="1" max="1000">
                    <label>평점 (0.0-5.0):</label>
                    <input type="number" id="validationRating" value="4.5" step="0.1" min="0" max="5">
                    <button onclick="testValidation()">검증 테스트</button>
                </div>
                <div class="result" id="validationResult">결과가 여기에 표시됩니다.</div>
            </div>
        </div>

        <script>
            // API 호출 도우미 함수
            async function apiCall(url, options = {}) {
                try {
                    const response = await fetch(url, {
                        headers: {
                            'Content-Type': 'application/json',
                            ...options.headers
                        },
                        ...options
                    });
                    
                    const data = await response.json();
                    return { success: response.ok, data, status: response.status };
                } catch (error) {
                    return { success: false, data: { error: error.message }, status: 0 };
                }
            }

            // 결과 표시 도우미 함수
            function displayResult(elementId, result) {
                const element = document.getElementById(elementId);
                element.className = result.success ? 'result success' : 'result error';
                element.textContent = JSON.stringify(result.data, null, 2);
            }

            // 경로 매개변수 테스트
            async function testPathParams() {
                const itemId = document.getElementById('itemId').value;
                const result = await apiCall(`/path/items/${itemId}`);
                displayResult('pathResult', result);
            }

            async function testFilePath() {
                const filePath = document.getElementById('filePath').value;
                const result = await apiCall(`/path/files/${filePath}`);
                displayResult('pathResult', result);
            }

            // 쿼리 매개변수 테스트
            async function testQueryParams() {
                const query = document.getElementById('searchQuery').value;
                const limit = document.getElementById('limitQuery').value;
                const result = await apiCall(`/query/search?q=${encodeURIComponent(query)}&limit=${limit}`);
                displayResult('queryResult', result);
            }

            async function testUserFilter() {
                const userType = document.getElementById('userFilter').value;
                const active = document.getElementById('activeFilter').value;
                const result = await apiCall(`/query/users?user_type=${userType}&active=${active}`);
                displayResult('queryResult', result);
            }

            // 요청 본문 테스트
            async function testCreateUser() {
                const userData = {
                    name: document.getElementById('userName').value,
                    email: document.getElementById('userEmail').value,
                    age: parseInt(document.getElementById('userAge').value)
                };
                
                const result = await apiCall('/body/users', {
                    method: 'POST',
                    body: JSON.stringify(userData)
                });
                displayResult('bodyResult', result);
            }

            // 중첩 모델 테스트
            async function testNestedModel() {
                try {
                    const offerData = JSON.parse(document.getElementById('offerData').value);
                    const result = await apiCall('/nested/offers', {
                        method: 'POST',
                        body: JSON.stringify(offerData)
                    });
                    displayResult('nestedResult', result);
                } catch (error) {
                    displayResult('nestedResult', { success: false, data: { error: 'Invalid JSON: ' + error.message } });
                }
            }

            // 숫자 검증 테스트
            async function testValidation() {
                const id = document.getElementById('validationId').value;
                const rating = document.getElementById('validationRating').value;
                const result = await apiCall(`/validation/items/${id}?rating=${rating}`);
                displayResult('validationResult', result);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# 4. 애플리케이션 시작 이벤트
@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행되는 이벤트"""
    print("🚀 FastAPI 학습 서버가 시작되었습니다!")
    print("📖 API 문서: http://localhost:8000/docs")
    print("🧪 클라이언트 테스트: http://localhost:8000/client")

@app.on_event("shutdown") 
async def shutdown_event():
    """서버 종료 시 실행되는 이벤트"""
    print("👋 FastAPI 학습 서버가 종료됩니다.")

if __name__ == "__main__":
    import uvicorn
    print("FastAPI 학습 서버를 시작합니다...")
    print("브라우저에서 http://localhost:8000 을 확인하세요!")
    uvicorn.run(
        "main:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )