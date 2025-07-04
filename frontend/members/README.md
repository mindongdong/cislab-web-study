# 🛠️ Git 사용 가이드

이 문서는 스터디 참여자가 `frontend/members/본인이름/` 폴더에 본인의 학습 결과물을 관리하기 위한 Git 사용 절차를 안내합니다.

## 1. 기본 세팅

```bash
# 최초 1회
$ git clone https://github.com/CISLAB-git-id/cislab-web-study.git
$ cd cislab-web-study

# 매 작업 전 최신 main 동기화
$ git checkout main
$ git pull origin main
```

## 2. 브랜치 규칙

`fe/이름/주차-주제`

- **fe**: frontend 작업을 의미합니다.
- **이름**: 영문 이름 혹은 GitHub ID
- **주차-주제**: 예) `week1-react`, `week2-form`

> 예시: `fe/choi-seonmi/week1-react`

## 3. 작업 순서

1. 작업 브랜치 생성 및 이동
   ```bash
   $ git checkout -b fe/choi-seonmi/week1-react
   ```
2. 코드·문서 작성 및 수정
3. 변경 파일 스테이징
   ```bash
   $ git add .
   ```
4. 커밋 메시지 작성
   ```bash
   $ git commit -m "[FE] Week1: React 컴포넌트 학습 정리"
   ```
5. 원격 브랜치 푸시 (최초 1회 `-u` 옵션)
   ```bash
   $ git push -u origin fe/choi-seonmi/week1-react
   ```
6. GitHub 웹에서 Pull Request(PR) 생성
   - **base**: `main`
   - **compare**: `fe/choi-seonmi/week1-react`
   - PR 템플릿에 작업 내용, 스크린샷, 참고 링크 작성
7. 코드 리뷰 & `Squash and Merge` 완료 시 로컬 main 동기화 및 브랜치 정리
   ```bash
   $ git checkout main
   $ git pull origin main
   $ git branch -d fe/choi-seonmi/week1-react
   $ git push origin --delete fe/choi-seonmi/week1-react
   ```

## 4. 디렉터리 구조 예시

```
frontend/
└── members/
    └── choi-seonmi/
        ├── README.md
        ├── week1/
        │   ├── README.md
        │   └── Todo.tsx
        └── week2/
```

## 5. 자주 쓰는 명령어

```bash
git status             # 변경 사항 확인
git log --oneline      # 커밋 로그 확인
git diff               # 상세 변경 내용 확인
git stash              # 임시 저장
git switch -c <name>   # 브랜치 생성 및 이동 (git 2.23+)
```

## 6. 커밋 & PR 템플릿 예시

```
[FE] Week2: 브라우저 저장소 활용 과제 완료

### 주요 내용
- 로컬 스토리지 CRUD 유틸 추가
- Custom Hook `useLocalStorage` 구현

### 스크린샷
> 이미지 첨부
```

> 커밋은 의미 단위로 작게 여러 번 하는 것을 권장합니다.
