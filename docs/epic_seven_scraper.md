# 에픽세븐 API 스크래퍼 (`epic_seven_api_scraper.py`)

이 문서는 에픽세븐 게임의 뉴스 데이터를 수집하는 `epic_seven_api_scraper.py`의 구조와 기능, 주요 특징을 설명합니다.

## 1. 개요

`EpicSevenApiScraper`는 OnStove의 공식 API를 사용하여 에픽세븐의 공지사항과 이벤트 정보를 수집합니다. 로드나인 스크래퍼와 마찬가지로 API를 직접 호출하여 효율성과 안정성이 높습니다.

- **게임**: 에픽세븐 (Epic Seven)
- **유형**: API 기반
- **클래스**: `EpicSevenApiScraper`

## 2. 핵심 동작 원리

스크래퍼는 카테고리(공지, 이벤트)별로 지정된 `board_seq` 값을 사용하여 OnStove API에 데이터를 요청합니다. API 응답은 JSON 형식이며, 이를 파싱하여 `GameNews` 객체의 리스트로 변환합니다.

### 2.1. 기본 URL

- **Base URL**: `https://api.onstove.com/cwms/v3.0`

### 2.2. API 엔드포인트

| 목적      | 엔드포인트                                      | HTTP Method |
| --------- | ----------------------------------------------- | ----------- |
| 목록 조회 | `/article_group/BOARD/{board_seq}/article/list` | `GET`       |

### 2.3. 보드 시퀀스 (`board_seq`)

각 뉴스 카테고리는 고유한 `board_seq` 값을 가집니다.

| 카테고리 | `board_seq`                     |
| -------- | ------------------------------- |
| 공지사항 | `995`                           |
| 이벤트   | `1000`                          |
| 업데이트 | `997` (코드 내 주석으로 언급됨) |

## 3. 주요 메서드

### `get_announcements()`

- **설명**: 공지사항 `board_seq` (995)를 사용하여 최신 공지 목록을 가져옵니다.
- **반환**: `List[GameNews]`

### `get_events()`

- **설명**: 이벤트 `board_seq` (1000)를 사용하여 최신 이벤트 목록을 가져옵니다.
- **반환**: `List[GameNews]`

### `get_news_detail(url: str)`

- **설명**: URL에서 `article_id`를 추출하지만, **현재 상세 내용을 가져오는 API 호출은 구현되어 있지 않습니다.** 항상 `None`을 반환합니다.
- **매개변수**:
  - `url` (str): 상세 페이지 URL (e.g., `https://page.onstove.com/epicseven/kr/view/123456`)
- **반환**: `None`

## 4. 데이터 파싱 및 처리

- **`_create_news_from_post()`**: API로부터 받은 개별 게시글 데이터를 `GameNews` 객체로 변환합니다.
- **HTTP 헤더**: 실제 브라우저와 유사한 상세한 헤더(`User-Agent`, `Referer`, `x-client-lang` 등)를 사용하여 API 요청을 보냅니다.
- **제목 장식**: 중요도(`📌`), 조회수(`🔥`), 카테고리(`📢`, `🎉`)에 따라 제목에 이모지를 추가하여 가독성을 높입니다.
- **날짜 처리**: API에서 받은 UNIX 타임스탬프(밀리초)를 `datetime` 객체로 변환합니다.

## 5. 특징 및 주의사항

- **미구현 기능**: `get_news_detail` 메서드는 상세 정보를 실제로 가져오지 않으므로, 목록 조회만 온전히 작동합니다.
- **동기식 HTTP 클라이언트**: `httpx.Client()`를 사용하여 동기적으로 API를 호출합니다. (개선 시 `AsyncClient` 고려 가능)
- **고정된 페이지 사이즈**: API 요청 시 페이지당 20개의 게시글(`size=20`)을 가져오도록 고정되어 있습니다.
