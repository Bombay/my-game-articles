# 로드나인 API 스크래퍼 (`lordnine_api_scraper.py`)

이 문서는 `lordnine_api_scraper.py`의 작동 방식, 주요 구성 요소 및 사용법을 설명합니다.

## 1. 개요

로드나인(Lordnine) 게임의 공지사항과 이벤트 소식을 수집하는 API 기반 스크래퍼입니다. OnStove의 공식 JSON API를 직접 호출하여 데이터를 가져오므로, HTML 파싱 방식보다 빠르고 안정적입니다.

- **게임**: 로드나인 (Lordnine)
- **유형**: API 기반
- **클래스**: `LordnineApiScraper`
- **상속**: `BaseScraper`

## 2. 핵심 동작 원리

스크래퍼는 OnStove API 서버와 통신하여 공지사항, 이벤트 목록 및 상세 정보를 JSON 형식으로 수신합니다. 수신된 데이터는 `GameNews` 모델로 파싱되어 일관된 형식으로 반환됩니다.

### 2.1. 기본 URL

모든 API 요청의 기본이 되는 URL입니다.

- **Base URL**: `https://api.onstove.com`

### 2.2. API 엔드포인트

| 목적          | 엔드포인트                                            | HTTP Method |
| ------------- | ----------------------------------------------------- | ----------- |
| 공지사항 목록 | `/cwms/v3.0/article_group/BOARD/128074/article/list`  | `GET`       |
| 이벤트 목록   | `/cwms/v.3.0/article_group/BOARD/128451/article/list` | `GET`       |
| 상세 정보     | `/cwms/v3.0/article/{article_id}`                     | `GET`       |

### 2.3. 공통 파라미터

목록 조회 API 호출 시 공통적으로 사용되는 쿼리 파라미터입니다.

```json
{
  "interaction_type_code": "LIKE,DISLIKE,COMMENT,VIEW",
  "content_yn": "Y",
  "summary_yn": "Y",
  "sort_type_code": "LATEST",
  "headline_title_yn": "Y",
  "translation_yn": "N",
  "page": 1,
  "size": 24
}
```

## 3. 주요 메서드

### `get_announcements()`

- **설명**: 최신 공지사항 목록을 가져옵니다.
- **반환**: `List[GameNews]`

### `get_events()`

- **설명**: 진행 중인 이벤트 목록을 가져옵니다.
- **반환**: `List[GameNews]`

### `get_news_detail(url: str)`

- **설명**: 제공된 URL에 해당하는 뉴스의 상세 정보를 가져옵니다. URL에서 `article_id`를 추출하여 상세 정보 API를 호출합니다.
- **매개변수**:
  - `url` (str): `https://page.onstove.com/l9/global/view/{article_id}` 형식의 상세 페이지 URL
- **반환**: `Optional[GameNews]`

## 4. 데이터 파싱 로직

- **`_parse_article_data()`**: 목록 API 응답의 개별 게시글 데이터를 `GameNews` 객체로 변환합니다.
- **`_parse_article_detail()`**: 상세 정보 API 응답을 `GameNews` 객체로 변환하며, HTML 본문을 포함한 전체 정보를 채웁니다.
- **`_extract_article_id_from_url()`**: 사용자에게 제공되는 웹 페이지 URL에서 API 호출에 필요한 `article_id`를 정규표현식을 이용해 추출합니다.
- **날짜 처리**: API 응답의 UNIX 타임스탬프(밀리초)를 `datetime` 객체로 변환합니다.

## 5. 특징 및 주의사항

- **User-Agent**: 실제 브라우저와 유사한 `User-Agent` 헤더를 사용하여 차단을 방지합니다.
- **중요도**: 게시글 제목에 '공지', '점검' 등의 키워드가 포함되거나, API에서 '고정'으로 표시된 경우 중요 게시물(`is_important=True`)로 판단합니다.
- **태그**: 제목과 API 응답의 `headline_title_name`(말머리) 필드를 분석하여 '공지', '이벤트', '점검' 등의 태그를 추출합니다.
