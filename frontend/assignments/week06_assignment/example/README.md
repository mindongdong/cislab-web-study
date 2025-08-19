# 독서 기록장 고도화 - Week 6 Assignment Solution

## 📚 프로젝트 개요

5회차에서 만든 독서 기록장을 React의 고급 기능들을 활용하여 업그레이드한 프로젝트입니다.

## ✨ 구현된 기능

### 1. 라이프사이클 활용 (useEffect) ✅
- **로컬스토리지 연동**: 책 목록이 자동으로 브라우저에 저장되며 새로고침해도 유지됩니다
- **독서 통계 자동 계산**: 총 독서 권수, 평균 별점, 완독 권수, 즐겨찾기 수 실시간 계산
- **최고 평점 도서 하이라이트**: 가장 높은 별점을 받은 책 자동 표시

### 2. useReducer로 상태 관리 ✅
- **BookReducer 구현**: 모든 책 관련 상태를 중앙에서 관리
- **액션 타입 정의**:
  - `ADD_BOOK`: 새 책 추가
  - `DELETE_BOOK`: 책 삭제
  - `UPDATE_BOOK`: 책 정보 수정
  - `TOGGLE_FAVORITE`: 즐겨찾기 토글
  - `UPDATE_STATUS`: 읽기 상태 변경
  - `LOAD_BOOKS`: 책 목록 로드
  - 필터링 관련 액션들

### 3. 최적화 기법 적용 ✅
- **useMemo 활용**:
  - `statistics`: 독서 통계 계산 최적화
  - `filteredBooks`: 필터링된 책 목록 계산 최적화
- **React.memo 활용**:
  - `BookItem`: 개별 책 카드의 불필요한 리렌더링 방지
  - `BookList`: 목록 컴포넌트 최적화
  - `SearchFilter`: 검색/필터 컴포넌트 최적화
  - `BookForm`: 폼 컴포넌트 최적화
- **useCallback 활용**:
  - 모든 dispatch 함수들을 메모이제이션
  - 자식 컴포넌트에 전달되는 이벤트 핸들러 최적화

### 4. Context API 구현 ✅
- **BookContext**:
  - 책 목록과 dispatch 함수 전역 관리
  - Props drilling 완전 제거
  - 커스텀 훅 `useBooks()` 제공
- **ThemeContext**:
  - 다크모드/라이트모드 테마 전환
  - 사용자 테마 설정 로컬스토리지 저장
  - 시스템 테마 자동 감지
- **Context 분리**:
  - 데이터와 테마를 별도 Context로 관리
  - 불필요한 리렌더링 최소화

### 5. 추가 기능 구현 ✅
- **검색 기능**: 제목/저자로 실시간 검색
- **필터링 기능**:
  - 읽기 상태별 필터 (읽을 예정/읽는 중/완독)
  - 별점별 필터 (1점~5점 이상)
  - 즐겨찾기만 보기 옵션
- **읽기 상태 관리**:
  - 읽을 예정 (toRead)
  - 읽는 중 (reading)
  - 완독 (completed)
  - 상태별 아이콘 및 배지 표시

## 📂 프로젝트 구조

```
example/
├── App.jsx                 # 메인 앱 컴포넌트
├── App.css                 # 스타일 (테마 변수 포함)
├── context/
│   ├── BookContext.jsx     # 책 상태 관리 Context
│   └── ThemeContext.jsx    # 테마 관리 Context
├── reducers/
│   └── bookReducer.js      # 책 상태 리듀서
└── components/
    ├── Header.jsx          # 헤더 (통계, 테마 토글)
    ├── SearchFilter.jsx    # 검색 및 필터 컴포넌트
    ├── BookForm.jsx        # 책 추가 폼
    ├── BookList.jsx        # 책 목록 컨테이너
    └── BookItem.jsx        # 개별 책 아이템
```

## 🎨 테마 시스템

CSS 변수를 활용한 다크/라이트 모드:
- 자동 시스템 테마 감지
- 사용자 선택 로컬스토리지 저장
- 부드러운 전환 애니메이션

## 🚀 성능 최적화 포인트

1. **컴포넌트 메모이제이션**: React.memo로 불필요한 리렌더링 방지
2. **계산 최적화**: useMemo로 비용이 큰 계산 캐싱
3. **함수 재생성 방지**: useCallback으로 함수 참조 유지
4. **Context 분리**: 관심사별 Context 분리로 리렌더링 최소화
5. **상태 불변성**: 리듀서에서 올바른 불변 업데이트 패턴 사용

## 🔍 주요 학습 포인트

1. **useReducer vs useState**: 복잡한 상태 로직을 리듀서로 관리하는 이점
2. **Context API 활용**: Props drilling 해결과 전역 상태 관리
3. **React 최적화 기법**: memo, useMemo, useCallback의 적절한 사용
4. **라이프사이클 관리**: useEffect로 사이드 이펙트 처리
5. **테마 시스템 구현**: CSS 변수와 Context를 활용한 테마 전환

## 💡 추가 개선 가능 사항

- CSV/JSON 형식으로 책 목록 내보내기/가져오기
- 읽기 목표 설정 및 진행률 표시
- 책 표지 이미지 URL 추가 기능
- 정렬 기능 (제목순, 저자순, 별점순, 최신순)
- 페이지네이션 또는 무한 스크롤

## 🎯 평가 기준 충족 사항

✅ **useEffect 활용** (20점)
- 로컬스토리지 연동 완벽 구현
- 사이드 이펙트 적절한 처리
- 의존성 배열 올바르게 설정

✅ **useReducer 구현** (20점)
- reducer 함수 올바른 구현
- 액션 타입 명확한 정의 및 활용
- 복잡한 상태 로직 체계적 관리

✅ **최적화 기법** (20점)
- useMemo로 통계 및 필터링 최적화
- React.memo로 컴포넌트 리렌더링 최적화
- useCallback으로 함수 재생성 방지

✅ **Context API** (20점)
- BookContext와 ThemeContext 분리 구현
- Provider 계층 구조화
- Props drilling 완전 해결

✅ **추가 기능** (10점)
- 검색/필터링 기능 완벽 구현
- 테마 전환 기능 구현
- 읽기 상태 관리 추가

✅ **코드 품질** (10점)
- 명확한 컴포넌트 구조 및 파일 구성
- 높은 코드 가독성 및 재사용성
- 일관된 코딩 스타일