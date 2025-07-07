<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# FastAPI 입문 강의 자료

## 1. 가상환경(venv, conda)을 왜 세팅해야 하는가?

- **의존성 관리**
프로젝트마다 필요한 패키지(라이브러리)와 버전이 다를 수 있습니다. 가상환경을 사용하면 프로젝트별로 독립적으로 패키지를 설치할 수 있어, 서로 다른 프로젝트 간의 충돌을 방지할 수 있습니다[^1][^2].
- **재현성 보장**
개발, 테스트, 배포 환경에서 동일한 패키지와 버전으로 실행할 수 있으므로, "내 컴퓨터에서는 되는데?" 문제를 예방할 수 있습니다.
가상환경을 사용하면 다른 개발자나 서버에서도 동일한 환경을 쉽게 구축할 수 있습니다[^1][^3].
- **시스템 환경 보호**
패키지를 전역(시스템 전체)에 설치할 경우, 다른 프로젝트나 시스템 자체에 영향을 줄 수 있습니다. 가상환경을 사용하면 시스템 파이썬 환경을 오염시키지 않습니다.
- **venv와 conda의 차이**
    - **venv**: 파이썬 표준 라이브러리로, 파이썬 프로젝트에 특화된 가상환경을 간단하게 만들 수 있습니다.
    - **conda**: 파이썬뿐 아니라 다양한 언어와 패키지(특히 데이터 과학, 과학 컴퓨팅 분야)를 관리할 수 있는 강력한 환경/패키지 매니저입니다. 복잡한 의존성이나 비파이썬 패키지까지 관리가 필요할 때 유용합니다[^1][^2].


## 2. Uvicorn이란 무엇인가?

- **ASGI 서버**
Uvicorn은 Python의 비동기 웹 프레임워크(예: FastAPI, Starlette 등)를 실행하기 위한 ASGI(Asynchronous Server Gateway Interface) 표준을 지원하는 웹 서버입니다[^4][^5][^6].
- **역할**
    - 클라이언트(브라우저 등)로부터 HTTP 요청을 받아 FastAPI 애플리케이션에 전달하고, 응답을 다시 클라이언트로 전송합니다.
    - 네트워크 통신, 연결 관리 등 저수준 작업을 처리하며, FastAPI는 비즈니스 로직과 HTTP 처리에 집중할 수 있게 해줍니다[^5].
    - 비동기(Async) 처리를 지원해, 동시에 여러 요청을 효율적으로 처리할 수 있습니다.
- **왜 필요한가?**
FastAPI는 웹 애플리케이션의 구조와 로직을 담당하지만, 실제로 네트워크를 통해 요청을 받고 응답을 보내는 역할은 Uvicorn 같은 서버가 담당합니다.
Uvicorn은 FastAPI와 궁합이 좋아 공식적으로 권장되는 서버입니다[^4][^5].


## 3. URL은 어떻게 구성되어 있는가?

- **URL(Uniform Resource Locator)의 기본 구조**
URL은 인터넷에서 특정 자원(웹페이지, 이미지 등)의 위치를 가리키는 주소입니다.
기본 구조는 다음과 같습니다:

```
scheme://subdomain.domain.tld:port/path?query#fragment
```

| 구성 요소 | 설명 | 예시 |
| :-- | :-- | :-- |
| scheme | 프로토콜(통신 방식) | http, https, ftp 등 |
| subdomain | (선택) 도메인 앞에 붙는 하위 영역 | www, api, blog 등 |
| domain | 메인 도메인 이름 | example.com |
| top-level domain | 최상위 도메인 | .com, .net, .kr 등 |
| port | (선택) 서버의 포트 번호 | :8000, :443 등 |
| path | 서버 내 자원의 경로 | /, /about, /blog/post-1 등 |
| query | (선택) 추가 정보(파라미터) | ?id=123\&sort=desc |
| fragment | (선택) 문서 내 특정 위치(앵커) | \#section2 |

- **예시**

```
https://api.example.com:8000/users?id=1#profile
```

    - https: 프로토콜
    - api: 서브도메인
    - example.com: 도메인
    - 8000: 포트
    - /users: 경로
    - id=1: 쿼리 파라미터
    - \#profile: 프래그먼트(문서 내 위치)
- **실제 FastAPI 예시**

```
http://127.0.0.1:8000/
```

    - http: 프로토콜
    - 127.0.0.1: 도메인(로컬호스트)
    - 8000: 포트
    - /: 루트 경로

FastAPI에서는 각 경로(path)에 대해 함수(엔드포인트)를 매핑하여 동작하게 됩니다[^7][^8][^9][^10].

이 자료를 바탕으로 FastAPI 실습 및 개념 설명을 체계적으로 진행할 수 있습니다.

<div style="text-align: center">⁂</div>

[^1]: https://www.gitpod.io/blog/venv-vs-conda-which-to-choose

[^2]: https://mindthevirt.com/venv-vs-conda-choosing-the-right-python-environment-manager-for-you/

[^3]: https://mapreader.readthedocs.io/en/v1.4.1/in-depth-resources/coding-basics/virtual-environments.html

[^4]: https://www.geeksforgeeks.org/python/fastapi-uvicorn/

[^5]: https://sentry.io/answers/understand-the-purpose-of-uvicorn-in-fastapi-applications/

[^6]: https://www.uvicorn.org

[^7]: https://fastapi.tiangolo.com/tutorial/first-steps/

[^8]: https://www.semrush.com/blog/what-is-a-url/

[^9]: https://www.concretecms.com/about/blog/devops/breaking-down-the-parts-of-a-url

[^10]: https://blog.hubspot.com/marketing/parts-url

[^11]: https://fastapi.tiangolo.com/ko/tutorial/first-steps/

[^12]: https://www.tutorialspoint.com/fastapi/fastapi_hello_world.htm

[^13]: https://jandari91.github.io/posts/fastapi_start/

[^14]: https://hyundoil.tistory.com/389

[^15]: https://www.youtube.com/watch?v=OYcdKUyX9-k

[^16]: https://dev.to/ceb10n/understanding-uvicorn-4gi8

[^17]: https://calmcode.io/course/fastapi/hello-world

[^18]: https://code.visualstudio.com/docs/python/tutorial-fastapi

[^19]: https://www.linkedin.com/pulse/why-you-should-configure-python-virtual-environments-conda-helmuth

[^20]: https://www.hostinger.com/tutorials/what-is-a-url

