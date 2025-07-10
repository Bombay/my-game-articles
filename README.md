# 게임 뉴스 수집 MCP 서버

3개 게임(에픽세븐, 로스트아크, 로드나인)의 뉴스 정보를 수집하는 MCP 서버

## 🎯 프로젝트 개요

이 프로젝트는 Model Context Protocol (MCP) 서버를 사용하여 다음 게임들의 뉴스 정보를 수집합니다:

- **로드나인** (OnStove API)
- **에픽세븐** (OnStove API)
- **로스트아크** (웹 스크래핑)

## 🔧 제공 도구

총 6개의 도구를 제공합니다 (game 파라미터로 게임 구분):

1. `get_game_announcements` - 공지사항 리스트
2. `get_announcement_detail` - 공지사항 상세
3. `get_game_events` - 이벤트 리스트
4. `get_event_detail` - 이벤트 상세
5. `get_game_updates` - 업데이트 리스트
6. `get_update_detail` - 업데이트 상세

## 🚀 설치 및 실행

### 1. 가상환경 생성

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. Playwright 브라우저 설치 (로스트아크용)

```bash
playwright install chromium
```

### 4. 서버 실행

```bash
python -m src.server
```

## 📋 개발 상태

현재 개발 진행 중입니다. 자세한 진행 상황은 [프로젝트 진행 상황](../plan/game-news-mcp/project_progress.md)을 참고하세요.

## 🛠️ 기술 스택

- **Python**: 3.9+
- **MCP SDK**: Anthropic MCP Python SDK
- **HTTP Client**: httpx (async 지원)
- **브라우저 자동화**: playwright (로스트아크용)
- **데이터 검증**: pydantic

## 📁 프로젝트 구조

```
my-game-articles/
├── src/
│   ├── server.py              # MCP 서버 메인
│   ├── config/
│   │   └── settings.py        # 설정 파일
│   ├── models/
│   │   └── game_news.py       # 데이터 모델
│   ├── scrapers/
│   │   ├── base.py           # 기본 스크래퍼
│   │   ├── lordnine.py       # 로드나인 스크래퍼
│   │   ├── epic_seven.py     # 에픽세븐 스크래퍼
│   │   └── lost_ark.py       # 로스트아크 스크래퍼
│   ├── handlers/
│   │   ├── base.py           # 기본 핸들러
│   │   ├── lordnine.py       # 로드나인 핸들러
│   │   ├── epic_seven.py     # 에픽세븐 핸들러
│   │   └── lost_ark.py       # 로스트아크 핸들러
│   └── utils/
│       └── helpers.py        # 유틸리티 함수
├── tests/                     # 테스트 파일
├── requirements.txt           # 의존성 목록
└── README.md                  # 이 파일
```

## 📄 라이센스

MIT License
