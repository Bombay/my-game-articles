# 게임 뉴스 MCP 서버 사용 가이드

이 프로젝트는 게임 뉴스 수집을 위한 MCP(Model Context Protocol) 서버를 제공합니다.

## 🚀 빠른 시작

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Playwright 브라우저 설치

```bash
playwright install
```

### 3. MCP 서버 테스트

```bash
python -m src.server
```

## 📋 지원하는 도구들

### 공지사항 관련

- `get_game_announcements`: 게임별 최신 공지사항 목록 조회
- `get_announcement_detail`: 특정 공지사항의 상세 정보 조회

### 이벤트 관련

- `get_game_events`: 게임별 최신 이벤트 목록 조회
- `get_event_detail`: 특정 이벤트의 상세 정보 조회

### 업데이트 관련

- `get_game_updates`: 게임별 최신 업데이트 목록 조회
- `get_update_detail`: 특정 업데이트의 상세 정보 조회

## 🎮 지원 게임

- `lordnine`: 로드나인
- `epic_seven`: 에픽세븐
- `lost_ark`: 로스트아크

## 🔧 Claude Desktop 설정

Claude Desktop에서 사용하려면 다음 설정을 추가하세요:

### macOS 경로

```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows 경로

```
%APPDATA%\Claude\claude_desktop_config.json
```

### 설정 내용

```json
{
  "globalShortcut": "",
  "mcpServers": {
    "game-news-scraper": {
      "command": "/Users/hyuntkim/workspace/my-game-articles/.venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/Users/hyuntkim/workspace/my-game-articles",
      "env": {
        "PYTHONPATH": "/Users/hyuntkim/workspace/my-game-articles"
      }
    }
  }
}
```

> **주의**: `cwd`와 `PYTHONPATH`의 경로를 본인의 프로젝트 경로로 수정하세요.

## 📚 사용 예시

### 1. 로드나인 공지사항 조회

```
로드나인의 최신 공지사항을 알려주세요.
```

### 2. 에픽세븐 이벤트 확인

```
에픽세븐의 진행 중인 이벤트를 확인해주세요.
```

### 3. 로스트아크 업데이트 정보

```
로스트아크의 최신 업데이트 정보를 가져와주세요.
```

## 🛠️ 개발자 도구

### MCP 서버 직접 실행

```bash
python -m src.server
```

### 디버그 모드 실행

```bash
LOG_LEVEL=DEBUG python -m src.server
```

### 테스트 실행

```bash
pytest tests/ -v
```

## 📞 문제 해결

### 1. 임포트 오류

- `PYTHONPATH` 환경변수가 올바르게 설정되었는지 확인
- 가상환경이 활성화되었는지 확인

### 2. 브라우저 오류

- Playwright 브라우저가 설치되었는지 확인: `playwright install`

### 3. 권한 오류

- 프로젝트 디렉토리의 읽기/쓰기 권한 확인

## 🔍 로그 확인

MCP 서버는 기본적으로 INFO 레벨의 로그를 출력합니다. 더 자세한 로그를 보려면:

```bash
LOG_LEVEL=DEBUG python -m src.server
```

## 📈 성능 최적화

- 동시 요청 수 제한: 기본 3개
- 타임아웃 설정: 기본 30초
- 캐시 활용으로 응답 속도 향상

## 🔄 업데이트

새로운 기능이나 버그 수정이 있을 때:

1. Git에서 최신 코드 가져오기
2. 의존성 업데이트: `pip install -r requirements.txt --upgrade`
3. Claude Desktop 재시작

이제 Claude Desktop에서 게임 뉴스를 쉽게 조회할 수 있습니다! 🎉
