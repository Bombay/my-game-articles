# 로스트아크 동적 스크래퍼 (`lost_ark_dynamic_scraper.py`)

이 문서는 `lost_ark_dynamic_scraper.py`의 작동 방식, 주요 구성 요소, 그리고 동적 스크래핑의 특징을 설명합니다.

## 1. 개요

로스트아크(Lost Ark) 공식 홈페이지의 뉴스 데이터를 수집하는 동적 스크래퍼입니다. 공식 홈페이지는 JavaScript를 통해 콘텐츠를 동적으로 로드하기 때문에, API 스크래퍼와 달리 `Playwright`라는 브라우저 자동화 도구를 사용하여 실제 웹 브라우저를 구동시켜 페이지를 렌더링한 후 HTML에서 직접 데이터를 추출합니다.

- **게임**: 로스트아크 (Lost Ark)
- **유형**: 동적 (Playwright 기반)
- **클래스**: `LostArkDynamicScraper`
- **상속**: `BaseScraper`

## 2. 핵심 동작 원리

1.  **브라우저 실행**: `Playwright`를 통해 가상 브라우저(Headless Chromium)를 실행합니다.
2.  **페이지 이동**: 목표 URL(공지, 이벤트, 업데이트)로 이동합니다.
3.  **콘텐츠 대기**: `wait_until='networkidle'` 옵션을 사용하여 페이지 내 모든 동적 콘텐츠(JavaScript)가 로드될 때까지 대기합니다.
4.  **HTML 파싱**: 렌더링이 완료된 페이지의 HTML 구조를 분석하여 CSS 선택자를 통해 원하는 데이터(제목, 링크, 날짜, 본문 등)를 추출합니다.
5.  **데이터 정제**: 추출한 데이터를 `GameNews` 모델에 맞게 정제하여 반환합니다.

### 2.1. 기본 URL

- **Base URL**: `https://lostark.game.onstove.com`

### 2.2. 대상 경로

| 목적     | 경로                                      |
| -------- | ----------------------------------------- |
| 공지사항 | `/News/Notice/List`                       |
| 이벤트   | `/News/Event/Now`                         |
| 업데이트 | `/News/Update/List`                       |
| 점검     | `/News/Notice/List` (공지사항에서 필터링) |

## 3. 주요 메서드

### `get_announcements()`, `get_events()`, `get_updates()`

- **설명**: 각 카테고리에 맞는 최신 게시글 목록을 가져옵니다. 내부적으로 `_get_news_list_with_playwright`를 호출합니다.
- **반환**: `List[GameNews]`

### `get_maintenance()`

- **설명**: `get_announcements()`를 호출하여 모든 공지사항을 가져온 뒤, 제목에 '점검', 'maintenance' 등의 키워드가 포함된 게시글만 필터링하여 반환합니다.
- **반환**: `List[GameNews]`

### `get_news_detail(url: str)`

- **설명**: 상세 페이지 URL로 직접 접속하여 제목, 본문, 날짜 등의 상세 정보를 추출합니다.
- **강건한 선택자 전략**: 여러 개의 가능한 CSS 선택자 목록(`title_selectors`, `content_selectors`, `date_selectors`)을 순차적으로 시도하여, 웹사이트 구조가 일부 변경되더라도 데이터를 안정적으로 추출할 수 있도록 설계되었습니다.
- **반환**: `Optional[GameNews]`

## 4. 데이터 추출 전략

- **목록 추출 (`_get_news_list_with_playwright`)**: 게시물 목록을 감싸는 컨테이너(`ul`, `tbody` 등)를 찾고, 그 안의 각 항목(`li`, `tr`)에서 `<a>` 태그를 찾아 제목과 링크를 추출합니다.
- **상세 내용 추출 (`get_news_detail`)**: 여러 CSS 선택자를 순서대로 시도하여 제목, 내용, 날짜를 찾습니다. 이는 웹사이트의 HTML 구조 변경에 대한 대응력을 높입니다.
- **카테고리 식별 (`_determine_category_from_url`)**: 현재 페이지의 URL 경로 문자열(`notice`, `event`, `update`)을 분석하여 뉴스 카테고리를 결정합니다.
- **중요도 식별**: 게시물에 `.notice`, `.important` 와 같은 특정 CSS 클래스가 적용되었는지 확인하여 중요 게시물을 판단합니다.

## 5. 특징 및 주의사항

- **성능**: 실제 브라우저를 구동하므로 API 기반 스크래퍼에 비해 속도가 느리고 더 많은 시스템 자원을 소모합니다.
- **안정성**: 웹사이트의 HTML 구조가 변경될 경우 스크래퍼가 오작동할 수 있습니다. (현재는 다중 선택자 전략으로 이를 완화)
- **점검 공지**: 점검 공지는 별도 페이지가 없어 공지사항 목록에서 키워드 필터링을 통해 추출하므로, 제목에 키워드가 없는 점검 공지는 누락될 수 있습니다.
