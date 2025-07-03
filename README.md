# CISLAB 웹 개발 스터디

<div align="center">

  <img style="width:40rem" src="https://cislab.cau.ac.kr/images/assets/logo.png"/>
  
  [![Frontend](https://img.shields.io/badge/Frontend-React-61DAFB?style=for-the-badge&logo=react&logoColor=white)](https://reactjs.org/)
  [![Backend](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  
</div>

## 📋 목차
- [소개](#-소개)
- [참여자](#-참여자)
- [스터디 규칙](#-스터디-규칙)
- [커리큘럼](#-커리큘럼)
- [팀 프로젝트](#-팀-프로젝트)
- [추천 강의](#-추천-강의)
- [프로젝트 구조](#-프로젝트-구조)

## 🎯 소개

CISLAB 웹 개발 스터디는 프론트엔드와 백엔드 개발을 학습하고, 실제 웹 서비스를 구현하는 것을 목표로 합니다. 

**✨ 핵심 목표**
- 웹 개발의 기초부터 실전까지 단계별 학습
- 프론트엔드(React)와 백엔드(FastAPI) 학습
- 팀 프로젝트를 통한 실무 경험
- 로그인/회원가입, 게시판, AI 챗봇 기능이 포함된 웹 서비스 개발

## 👥 참여자

| 이름 | 역할 | GitHub |
|------|------|--------|
| 최선미 | Frontend Developer | [@github](https://github.com/) |
| 김도균 | Frontend Developer | [@github](https://github.com/) |
| 오성진 | Backend Developer | [@github](https://github.com/) |
| 김진서 | Backend Developer | [@github](https://github.com/) |

## 📌 스터디 규칙

### 🗓️ 일정
- **스터디 주기**: 주 2회
- **시간**: 총 3시간
  - 1시간: 공통 세션
  - 1시간: 백엔드 세션
  - 1시간: 프론트엔드 세션

### 📚 학습 방식
- **과제 및 발표 주도 학습**: 매 세션마다 과제 수행 및 발표 준비 필수
- **AI 활용 규칙**:
  - 개인 학습 시: 기술의 근본 원리 이해를 위해 **AI 툴 사용 지양** ⚠️
  - 팀 프로젝트 시: 개발 효율성을 위해 **AI 코딩 툴 적극 활용** ✅
- **기록 규칙**: 모든 학습 내용과 자료는 공유하여 아카이빙

## 📖 커리큘럼

### 🌐 공통 세션
| 주차 | 주제 |
|------|------|
| 0주차 | GitHub 규칙, VSCode 세팅 방법 |
| 1주차 | 웹 아키텍처 이해, 통신 규칙, 프론트엔드/백엔드 개요 |
| 2주차 | 인증/인가 개념 - 세션, 쿠키, JWT |

### ⚛️ 프론트엔드 세션
| 주차 | 주제 |
|------|------|
| 1주차 | 웹사이트 클론코딩, React 컴포넌트, Props, Hooks 기초 |
| 2주차 | Form 데이터 처리, 브라우저 저장소 활용 |
| 3주차 | 리마인드 (글쓰기 및 피드백) |
| 4-5주차 | 게시판 UI 구성, 테이블 개념, 페이지 라우팅 |
| 6-7주차 | 관리자 페이지, 권한 및 인증/인가 처리 |
| 8-9주차 | 챗봇 UI 구현, 상태관리 개념 |

### ⚡ 백엔드 세션
| 주차 | 주제 |
|------|------|
| 1주차 | FastAPI 서버 세팅, 경로 매개변수, 요청 데이터 처리 |
| 2주차 | 쿠키/폼/파일 처리, 관계형 DB 및 ERD 설계 |
| 3주차 | 리마인드 (글쓰기 및 피드백) |
| 4-5주차 | 게시판 CRUD API 설계, ORM을 통한 DB 연결 |
| 6-7주차 | 관리자 페이지 API, API 문서화, 에러 처리 |
| 8-9주차 | 외부 API 연동, LLM 기능 API 설계 |

## 🏆 팀 프로젝트

### 🎯 프로젝트 개요
- **시작 시기**: 스터디 4주차부터
- **목표**: 로그인/회원가입, 게시판, AI 챗봇 기능이 포함된 웹 서비스 개발

### 👥 팀 구성
| 팀 | 프론트엔드 | 백엔드 |
|----|-----------|--------|
| Team 1 | 최선미 | 오성진 |
| Team 2 | 김도균 | 김진서 |

### 📝 프로젝트 규칙
- Pull Request 시 코드 의도와 설명 필수 작성
- 코드 리뷰 후 merge 진행
- 매주 진행 상황공유

## 📚 추천 강의

### 프론트엔드
- [제로초 - 리액트 무료 강의](https://inf.run/LWuoL)

### 백엔드
- [FastAPI 공식문서 가이드](https://fastapi.tiangolo.com/ko/tutorial/first-steps/)

## 📁 프로젝트 구조

```
cislab-web-study/
│
├── 📂 common/                    # 공통 세션 자료
│   ├── week0/
│   ├── week1/
│   └── week2/
│
├── 📂 frontend/                  # 프론트엔드 자료
│   ├── lectures/                 # 강의 자료
│   ├── assignments/              # 과제
│   └── members/                  # 개인별 정리 자료
│       ├── choi-seonmi/
│       └── kim-dogyun/
│
├── 📂 backend/                   # 백엔드 자료
│   ├── lectures/                 # 강의 자료
│   ├── assignments/              # 과제
│   └── members/                  # 개인별 정리 자료
│       ├── oh-seongjin/
│       └── kim-jinseo/
│
├── 📂 resources/                 # 참고 자료
│   ├── references/
│   └── templates/
│
└── README.md
```
