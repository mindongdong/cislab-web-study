## React.js 실습 과제: 독서 기록장 고도화
---

- [Reading records_upgrade](https://playcode.io/2502137)

### 0. 컴포넌트 분리, CSS 파일 분리

### 1. 라이플사이클 활용 (useEffect)

- 로컬스토리지 연동 구현
    - 읽은 책의 목록을 로컬스토리지에 저장
        - `App.jsx`에서 `useEffect` 이용
        - 로컬 스토리지는 key-value 형식으로 데이터 저장. 데이터는 문자열 형식.   
        객체나 배열 같은 복잡한 데이터는 JSON으로 변환하여 저장하고, 가져오며 다시 파싱하는 과정 필요
        - Mount: 데이터를 불러오기
        - Update: `books`의 목록이 바뀔 때 마다 저장
    - localstorage
        ```jsx
        // 값 저장
        useEffect(()=> {
        localStorage.setItem("key", "value")
        })
        // 값 가져오기
        localStorage.getItem("key");
        // 값 삭제
        localStorage.removeItem('key')
        ```

- 독서 통계
    - `Booklist.jsx`에서 `useEffect` 이용
    - Update: `books`가 변할 때마다 실행
    - 총 독서 권수
    - 평균 별점
        - `reduce(callback, initialValue)`
    - 가장 높은 별점 받은 책 하이라이트
        - `Math.max`


### 2. 상태 관리 리팩토링 (useReducer)

- 책 추가 / 삭제 / 수정
    - `App.jsx`에서 `useReducer` 이용
        - `dispatch({type: "", payload: value})`
    1. 액션 타입 정의
    2. reducer 함수
    3. dispatch로 호출
- 즐겨찾기 토글
    - `Booklist.jsx`에 전달
    - `Bookitem.jsx`에 버튼 추가

### 3. 추가 기능

- 즐겨찾기만 보기
    - `Booklist.jsx`에 필터링 기능 추가

### 4. 최적화

- 연산 최적화
    - `Booklist.jsx`에서 즐겨찾기 필터링에 `useMemo` 사용
- 컴포넌트 리렌더링 최적화
    - 각 컴포넌트 마다 `React.memo` 사용
- 함수 재생성 방지
    - `App.jsx`에서 각 함수마다 적용

### 5. Context API 구현

- 전달을 위해 `createContext`, 받아오기 위해 `useContext`
- `BookContext`: 함수 관리 및 Props drilling
- `ThemeContext`로 