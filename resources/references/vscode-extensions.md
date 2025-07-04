# VSCode 필수 확장 프로그램 가이드

웹 개발 생산성과 코드 품질 향상을 위해 스터디원들이 설치하면 좋은 Visual Studio Code 확장 프로그램을 **공통**, **프론트엔드**, **백엔드**로 구분해 정리했습니다.

---

## 1. 공통 추천 확장 프로그램

| #   | 확장 프로그램                      | 핵심 기능                              |
| --- | ---------------------------------- | -------------------------------------- |
| 1   | Prettier – Code formatter          | 저장 시 코드 자동 정렬 및 포맷팅       |
| 2   | ESLint                             | JavaScript/TypeScript 린팅 & 자동 수정 |
| 3   | GitLens                            | Git blame·히스토리·커밋 비교           |
| 4   | Material Icon Theme / vscode-icons | 탐색기 아이콘 가독성 향상              |
| 5   | Path Intellisense                  | 파일 경로 자동 완성                    |
| 6   | Live Share                         | 실시간 공동 편집·디버깅                |
| 7   | Settings Sync                      | 확장 / 설정 / 키맵 클라우드 동기화     |
| 8   | Bracket Pair Colorizer 2\*         | 괄호 쌍 색상 구분 (\*최근 VSCode 내장) |
| 9   | Indent Rainbow                     | 들여쓰기 레벨 색상 표시                |
| 10  | Code Spell Checker                 | 코드·주석 오타 검사                    |
| 11  | Auto Rename Tag                    | 시작·종료 태그 동시 수정               |
| 12  | Korean Language Pack               | VSCode 한글 UI                         |

---

## 2. 프론트엔드(React 중심) 권장 확장

| #   | 확장 프로그램                          | 핵심 기능                          |
| --- | -------------------------------------- | ---------------------------------- |
| 1   | ES7+ React/Redux/React-Native Snippets | `rfc` 등 스니펫 자동 생성          |
| 2   | Tailwind CSS IntelliSense              | 클래스 자동 완성·하이라이트        |
| 3   | Styled-components (dcasella)           | CSS-in-JS 문법 색상 & IntelliSense |
| 4   | Prettier                               | 코드 스타일 일관 유지 (공통)       |
| 5   | ESLint                                 | 실시간 린팅·자동 고침 (공통)       |
| 6   | Live Server                            | HTML/CSS/JS 실시간 리로드          |
| 7   | Auto Close Tag / Auto Complete Tag     | 태그 자동 닫기·완성                |
| 8   | Color Highlight                        | HEX/RGB 색상 미리보기              |
| 9   | CSS Peek                               | HTML ↔ CSS 정의 빠른 이동          |

---

## 3. 백엔드(FastAPI & Python) 권장 확장

| #   | 확장 프로그램               | 핵심 기능                          |
| --- | --------------------------- | ---------------------------------- |
| 1   | Python (Microsoft)          | 인터프리터 선택·디버깅·테스팅      |
| 2   | Pylance                     | 고속 타입 체킹 · IntelliSense      |
| 3   | FastAPI – Snippets and more | 라우터·의존성 스니펫 자동 생성     |
| 4   | Thunder Client              | VSCode 내장 REST API 테스트        |
| 5   | Black Formatter / autopep8  | Python 코드 포맷터                 |
| 6   | Docker (Microsoft)          | 컨테이너 관리·디버깅               |
| 7   | GitLens / Prettier / ESLint | 버전관리·포맷팅·JS 린팅(풀스택 시) |
| 8   | Auto Docstring              | 함수/클래스 docstring 템플릿 생성  |
| 9   | SQLTools                    | DB 연결·쿼리 실행                  |

---

### 🗒️ 설치 순서 추천

1. VSCode 설치
2. **공통** 확장 프로그램 일괄 설치
3. 본인 역할(프론트엔드/백엔드)에 맞는 추가 확장 설치
4. `Settings Sync` 로 개인 설정 백업 및 동기화

> 이 리스트를 따라 세팅하면 코드 품질·생산성·협업 경험이 크게 향상됩니다. 필요에 따라 개인 선호 플러그인을 추가해 사용하세요.
