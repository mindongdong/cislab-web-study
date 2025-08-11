## React.js 실습 과제: 독서 기록장 고도화

### 📌 과제 개요

5회차에서 만든 독서 기록장을 **인프런 강의 섹션 8, 10, 11, 12**에서 학습한 내용을 활용하여 업그레이드합니다. 라이프사이클, useReducer, 최적화, Context API를 적용하여 더 완성도 높은 코드로 발전시키세요.

### 📋 요구사항

#### 1. 라이프사이클 활용 (useEffect)

- **로컬스토리지 연동**
    - 책 목록을 브라우저 로컬스토리지에 저장
    - 새로고침해도 데이터가 유지되도록 구현
    - 컴포넌트 마운트 시 로컬스토리지에서 데이터 불러오기
- **독서 통계 자동 계산**
    - 책 목록이 변경될 때마다 통계 자동 업데이트
    - 총 독서 권수, 평균 별점 표시
    - 가장 높은 별점을 받은 책 하이라이트

#### 2. useReducer로 상태 관리 리팩토링

- **BookReducer 구현**
    
    ```javascript
    // 액션 타입 예시const ACTION_TYPES = {  ADD_BOOK: 'ADD_BOOK',  DELETE_BOOK: 'DELETE_BOOK',  UPDATE_BOOK: 'UPDATE_BOOK',  LOAD_BOOKS: 'LOAD_BOOKS',  TOGGLE_FAVORITE: 'TOGGLE_FAVORITE'};
    ```
    
- useState 대신 useReducer로 책 목록 상태 관리
- 책 추가/삭제/수정 로직을 reducer로 이전
- **추가 기능**: 즐겨찾기 토글 기능 구현

#### 3. 최적화 적용

- **useMemo 활용**
    - 독서 통계 계산 최적화
    - 필터링된 책 목록 계산 최적화
- **React.memo 활용**
    - BookItem 컴포넌트 불필요한 리렌더링 방지
    - BookList 컴포넌트 최적화
- **useCallback 활용**
    - 이벤트 핸들러 함수들 최적화
    - 자식 컴포넌트에 전달되는 함수 재생성 방지

#### 4. Context API 구현

- **BookContext 생성**
    - 책 목록과 dispatch 함수 전역 관리
    - Props drilling 제거
- **ThemeContext 생성**
    - 다크모드/라이트모드 테마 전환 기능
    - 사용자 테마 설정 로컬스토리지 저장
- **Context 분리**
    - 데이터 Context와 테마 Context 분리
    - Provider 컴포넌트 구조화

#### 5. 추가 기능 구현

- **검색 및 필터링**
    - 제목/저자로 책 검색
    - 별점별 필터링
    - 즐겨찾기만 보기 옵션
- **읽기 상태 관리**
    - 읽는 중/완독/읽을 예정 상태 추가
    - 상태별 책 분류 및 표시

### 📊 컴포넌트 구조

```
App
├── Providers (Context Providers)
│   ├── BookProvider
│   └── ThemeProvider
├── Header
│   ├── ThemeToggle
│   └── Statistics
├── BookManager
│   ├── BookForm
│   ├── SearchFilter
│   └── BookList
│       └── BookItem
└── Footer
```

### 평가 기준

1. **useEffect 활용** (20점)
    
    - 로컬스토리지 연동 구현
    - 사이드 이펙트 적절한 처리
    - 클린업 함수 활용
2. **useReducer 구현** (20점)
    
    - reducer 함수 올바른 구현
    - 액션 타입 정의 및 활용
    - 복잡한 상태 로직 관리
3. **최적화 기법** (20점)
    
    - useMemo 적절한 활용
    - React.memo 올바른 적용
    - useCallback 효과적 사용
4. **Context API** (20점)
    
    - Context 생성 및 Provider 구현
    - Context 분리 및 구조화
    - Props drilling 해결
5. **추가 기능** (10점)
    
    - 검색/필터링 기능
    - 테마 전환 기능
6. **코드 품질** (10점)
    
    - 컴포넌트 구조 및 파일 구성
    - 코드 가독성 및 재사용성

### 💡 힌트

```javascript
// Reducer 구조 예시
function bookReducer(state, action) {
  switch (action.type) {
    case 'ADD_BOOK':
      return [...state, action.payload];
    case 'DELETE_BOOK':
      return state.filter(book => book.id !== action.payload);
    // ... 기타 액션들
    default:
      return state;
  }
}

// Context 구조 예시
const BookContext = createContext();
const ThemeContext = createContext();

// 최적화 예시
const statistics = useMemo(() => {
  return calculateStatistics(books);
}, [books]);

const MemoizedBookItem = React.memo(BookItem);
```

### 🎯 도전 과제 (선택사항)

- CSV/JSON 형식으로 책 목록 내보내기/가져오기
- 읽기 목표 설정 및 진행률 표시
- 책 표지 이미지 URL 추가 기능
- 정렬 기능 (제목순, 저자순, 별점순, 최신순)

### 📁 제출 방법

1. 프로젝트 핵심 코드를 [your-position]/members/[your-name]/week6 폴더에 업로드
2. README.md에 다음 내용 포함:
    - 구현한 기능 목록
    - 최적화 적용 부분 설명
    - 학습한 내용 중 가장 유용했던 부분

### ⏰ 제출 기한

- 8월 14일 목요일까지
