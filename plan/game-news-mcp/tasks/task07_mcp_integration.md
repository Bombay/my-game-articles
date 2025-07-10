# Task 07: MCP 서버 통합 및 핸들러 등록

## 📋 체크리스트

- [ ] 각 게임 스크래퍼를 MCP 서버에 연결
- [ ] 6개 도구 핸들러 구현
- [ ] 통합 에러 처리 및 응답 표준화
- [ ] 비동기 처리 최적화
- [ ] 도구별 메타데이터 및 설명 추가

## 📝 상세 내용

### 구현할 기능들

- 각 게임 스크래퍼를 MCP 서버 도구로 연결
- 일관된 도구 호출 인터페이스 구현
- 에러 발생 시 적절한 응답 반환
- 도구별 파라미터 검증

### 도구 목록 (총 6개)

```python
TOOLS = [
    "get_game_announcements",     # game 파라미터로 게임 구분
    "get_announcement_detail",    # game, url 파라미터
    "get_game_events",           # game 파라미터로 게임 구분
    "get_event_detail",          # game, url 파라미터
    "get_game_updates",          # game 파라미터로 게임 구분
    "get_update_detail"          # game, url 파라미터
]

SUPPORTED_GAMES = ["lordnine", "epic_seven", "lost_ark"]
```

## 🛠️ 기술적 세부사항

### 사용할 기술 스택

- **MCP SDK**: 도구 등록 및 핸들링
- **asyncio**: 비동기 처리
- **pydantic**: 파라미터 검증

### 파일 구조

```
my-game-articles/
├── src/
│   ├── server.py          # MCP 서버 메인
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── lordnine.py    # 로드나인 도구 핸들러
│   │   ├── epic_seven.py  # 에픽세븐 도구 핸들러
│   │   └── lost_ark.py    # 로스트아크 도구 핸들러
│   └── scrapers/
│       ├── lordnine.py    # 로드나인 스크래퍼
│       ├── epic_seven.py  # 에픽세븐 스크래퍼
│       └── lost_ark.py    # 로스트아크 스크래퍼
```

### 핵심 구현 요소

- **도구 핸들러**: 각 도구별 비동기 처리 함수
- **에러 핸들링**: 네트워크 오류, 파싱 오류 등 적절한 응답
- **응답 표준화**: 모든 도구가 일관된 JSON 형식 반환
- **성능 최적화**: 동시 요청 처리 및 캐싱

## ✅ 완료 조건

- [ ] 6개 도구가 모두 MCP 서버에 등록됨
- [ ] 각 도구가 올바른 응답을 반환함
- [ ] 에러 상황에서 적절한 메시지 반환
- [ ] 도구 메타데이터가 정확함
- [ ] 성능 요구사항 만족

### 검증 방법

```python
# MCP 서버 통합 테스트
from src.server import GameNewsServer

server = GameNewsServer()

# 도구 등록 확인
tools = server.list_tools()
assert len(tools) == 6
assert "get_game_announcements" in [tool.name for tool in tools]

# 각 도구 호출 테스트
for tool_name in TOOLS:
    for game in SUPPORTED_GAMES:
        try:
            if "detail" in tool_name:
                # 상세 도구는 game, url 파라미터 필요
                result = await server.call_tool(tool_name, {
                    "game": game,
                    "url": "https://example.com"
                })
            else:
                # 리스트 도구는 game 파라미터만 필요
                result = await server.call_tool(tool_name, {"game": game})

            assert result is not None
            print(f"✅ {tool_name} ({game}) 테스트 성공")
        except Exception as e:
            print(f"❌ {tool_name} ({game}) 테스트 실패: {e}")

# 성능 테스트
import time
start = time.time()
results = await asyncio.gather(*[
    server.call_tool("get_game_announcements", {"game": "lordnine"}),
    server.call_tool("get_game_announcements", {"game": "epic_seven"}),
    server.call_tool("get_game_announcements", {"game": "lost_ark"})
])
duration = time.time() - start
assert duration < 15  # 15초 이내 동시 처리
```
