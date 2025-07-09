# Task 02: MCP 서버 기본 구조 생성

## 📋 체크리스트
- [x] MCP 서버 메인 클래스 생성
- [x] 도구 등록 시스템 구현
- [x] 기본 설정 및 초기화 로직
- [x] 게임별 도구 그룹 구조 설계
- [x] 에러 핸들링 및 로깅 시스템

## 📝 상세 내용
### 구현할 기능들
- MCP 서버 기본 클래스 구현
- 6개 도구 등록 시스템 (game 파라미터로 게임 구분)
- 일관된 응답 형식 보장
- 비동기 처리 지원

### 코드 예시
```python
# src/server.py
from mcp.server import Server
from mcp.server.models import Tool
import asyncio

class GameNewsServer:
    def __init__(self):
        self.server = Server("game-news-mcp")
        self.setup_tools()
    
    def setup_tools(self):
        # 6개 도구 등록 (game 파라미터로 게임 구분)
        tools = [
            "get_game_announcements",
            "get_announcement_detail", 
            "get_game_events",
            "get_event_detail",
            "get_game_updates",
            "get_update_detail"
        ]
        
        for tool in tools:
            self.register_tool(tool)
```

## 🛠️ 기술적 세부사항
### 사용할 기술 스택
- **MCP Server**: 비동기 처리 지원
- **Pydantic**: 데이터 검증 및 직렬화
- **AsyncIO**: 비동기 웹 요청 처리

### 파일 구조
```
src/
├── server.py          # MCP 서버 메인 클래스
├── handlers/
│   ├── __init__.py
│   ├── lordnine.py    # 로드나인 도구 핸들러
│   ├── epic_seven.py  # 에픽세븐 도구 핸들러
│   └── lost_ark.py    # 로스트아크 도구 핸들러
└── config/
    ├── __init__.py
    └── settings.py     # 서버 설정
```

### 도구 명세
총 6개 도구 (game 파라미터로 게임 구분):
1. `get_game_announcements` - 공지사항 리스트 (game: lordnine|epic_seven|lost_ark)
2. `get_announcement_detail` - 공지사항 상세 (game, url)
3. `get_game_events` - 이벤트 리스트 (game: lordnine|epic_seven|lost_ark)
4. `get_event_detail` - 이벤트 상세 (game, url)
5. `get_game_updates` - 업데이트 리스트 (game: lordnine|epic_seven|lost_ark)
6. `get_update_detail` - 업데이트 상세 (game, url)

## ✅ 완료 조건
- [x] MCP 서버가 정상적으로 시작됨
- [x] 6개 도구가 모두 등록됨
- [x] 도구 목록 조회가 가능함
- [x] 기본 에러 핸들링이 동작함
- [x] 로깅 시스템이 구현됨

### 검증 방법
```bash
# 서버 시작 테스트
python -m src.server

# 도구 목록 확인
curl http://localhost:8000/tools

# 기본 도구 호출 테스트
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_game_announcements", "params": {"game": "lordnine"}}'
```