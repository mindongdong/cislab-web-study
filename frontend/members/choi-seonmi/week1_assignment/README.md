# CGV 홈페이지 클론코딩

## img

<img width="936" height="749" alt="Image" src="https://github.com/user-attachments/assets/e5aca271-bed3-4639-8b12-bc5b892dc35b" />

## 1. 메인 홈페이지 구조 짜기

- 전체적인 구조는 크게 header, main, popup, button, footer 로 나뉨
- 전부 `div`로 구성되어 있고, class로 설정되어 있음
    - `class=header`가 붙은 `<div>`태그를 시멘틱 태그 `<header>`로 바꿈. 클래스는 유지.
    - footer는 시멘틱 태그로 작성되어 있었음
    - `class=container`(실제 코드에서는 전부 contaniner라 오타가 나있음)의 태그는 `<main>`으로 바꿈
- class나 id등 이름은 똑같이 작성
- 주석도 따라서 표기
- `title`은 'clone CGV'
- css 파일은 `main.css`
- index.html
    ```html
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="main.css">
        <title>clone CGV</title>
    </head>
    <body>
        <div id="cgvwrap">
            <div class="cgv-ad-wrap" id="cgv_main_ad">

            </div>
            <!-- S Header -->
            <header class="header">
                <!-- S 서비스 메뉴 -->
                <div class="header_content"></div>
                <!-- E 서비스 메뉴 -->
                <!-- S 서브 메뉴 -->
                <nav class="nav" style="left:0px;">
                    <div class="contents">
                        <ul class="nav_menu">
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                            <li></li>
                        </ul>
                        <div class="totalSearch_wrap"></div>
                    </div>
                </nav>
                <!-- E 서브 메뉴 -->
            </header>
            <!-- E Header -->
            <!-- S Container -->
            <main class="container">
                <div id="ctl00_PlaceHolderContent_divMovieSelection_wrap" class="movieSelection_wrap">
                    <div class="contents"></div>
                </div>
                <div class="movieChartBeScreen_wrap">
                    <div class="contents"></div>
                </div>
                <div id="ctl00_PlaceHolderContent_event_wrap" class="event_wrap">
                    <div class="contents"></div>
                </div>

                <div class="specialHall_wrap">
                    <div class="contents"></div>
                </div>

                <div class="giftcon_wrap">
                    <div class="contents"></div>
                </div>

                <div class="noticeClient_wrap"></div>
            </main>
            <!-- E Container -->
            <!-- S Popup -->
            <div class="com_pop_wrap">
                <div class="com_pop_fog"></div>
            </div>
            <div class="pop_wrap">
                <div id="pop_supportOS" class="popup" style="display:none"></div>
                <div id="pop_supportBrower" class="popup" style="display:none"></div>
            </div>
            <!-- E Popup -->
            <!-- S 예매하기 및 TOP Fixed 버튼 -->
            <div class="fixedBtn_wrap topBtn"></div>
            <!-- E 예매하기 및 TOP Fixed 버튼 -->
            <!-- S Footer -->
            <Footer>
                <div id="BottomWrapper" class="sect-ad">

                </div>
                <ul class="policy_list"></ul>
                <article class="comany_info_wrap"></article>

                <div class="adFloat2" style="display:none"></div>
            </Footer>
                <!-- E Footer -->
        </div>


    </body>
    </html>
    ```

## 2. Header

### 서비스 메뉴
- html
    - 헤더의 왼쪽 부분 마크는 `<h1 onclick>`에 링크 `<a href="#">` 할당
        - 실제 웹사이트에서는 `<a href="/">`로 되어있지만 이렇게 하면 상위 디렉토리 페이지로 넘어가서 `#`으로 대체
            - `#`으로 대체하면 마크를 누를 시 다시 접속 된 링크에 '#'이 붙지만 `/`는 해당 링크로 다시 가는 것인지 링크에 별다른 표기가 생기지 않음
    - 헤더의 오른쪽 부분의 로그인, 회원가입 등의 메뉴는 `<ul>`로 구성
    - jquery 스크립트 추가
- css
    - 정렬
        - `header`에 `position: relative` 부여, 오른쪽 메뉴 글씨에 `position: absolute` 부여
        - 하위 `div`들에 `display`값 flex, inline-flex 등 사용
        - `contents`는 `justify-content: space-between` 통해 정렬: 메뉴들이 오른쪽에 붙게 됨
        - `align-item`의 `flex-end`, `center` 등

    - 기본 설정(태그 설정)
        - 제목의 폰트 고정
        - 폰트 패밀리 설정
        - `ol` 및 `ul`의 기본 점을 없애기 위해 `list-style: none;`

    - ad칸은 없앰
    - 옆 공간까지 꽉 차서 우선 `#cgvwrap`에 다음 코드 추가
        ```css
        #cgvwrap {
            max-width: 1200px;
            margin: 0 auto; 
            padding: 0 20px;
        }
        ```

### 서브 메뉴(nav)
- html
    - 서브 메뉴
        - `<dl>`태그 사용: 용어와 그에 대한 설명을 리스트 형식으로 정의할 때 사용
            - `<dt>`: 용어나 이름을 나타내는 요소
            - `<dd>`: 용어에 대한 설명을 나타내는 요소
        - `tabindex="-1"`: 상호작용이 가능한 요소라도 tab키로 인한 포커스가 이동하지 않음
    - 검색창
        - `<label for="">`: 요소 id를 넣어 라벨과 결합될 요소를 명시하는 for 속성
- css 
    - `nav`에 `absolute`를 사용하여 정렬
    - `nav`에 `:after`를 이용해 빨간 선 추가
    - 메뉴의 각 리스트는 `li:first-child`등을 사용하여 조정
    - `.nav_menu:has(*:focus-within) .nav_overMenu{display:block !important}`
        - 포커스가 올라갈 경우 `display: none` > `block`

## 3. Main

### moviesection
- html
    - 비디오창
        - 비디오태그 `<video>` 사용. 속성 `autoplay`, `muted` 추가
        - 링크를 가져오는 태그는 `<source>`
- css
    - 비디오가 부모 속성을 넘어 커지는 현상 발생
        - 부모 설정에 height 명확히
            ```css
            .movieSelection_wrap .contents {
            height: 100%;
            }
            ```
        - 비디오가 담긴 박스의 width를 줄이고, 중앙정렬
            ```css
            .movieSelection_wrap .contents .video_wrap {
                overflow: hidden;
                position: relative;
                width: 65%;
                height: 100%;
                margin: 0 auto;
            }
            ```

### movie chart
- html
    - `araia-label` 속성: 이미지를 사용해 텍스트 역할을 하게 함.
    - `<i>` 태그: 기본 텍스트로 구현할 수 없는 택스트를 구현할 때 사용. 이탤릭체 등. 이 페이지에서는 연령 표기, 스크린 타입