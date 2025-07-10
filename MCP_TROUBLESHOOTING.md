# MCP 서버 문제 해결 가이드

## ✅ 현재 서버 상태

### 🔧 **테스트 결과**

- ✅ MCP 서버 정상 시작
- ✅ **6개 도구 모두 정상 등록**
- ✅ JSON-RPC 통신 정상
- ✅ tools/list 요청 정상 응답

### 📋 **등록된 도구들**

1. `get_game_announcements` - 게임별 공지사항 목록
2. `get_announcement_detail` - 공지사항 상세 정보
3. `get_game_events` - 게임별 이벤트 목록
4. `get_event_detail` - 이벤트 상세 정보
5. `get_game_updates` - 게임별 업데이트 목록
6. `get_update_detail` - 업데이트 상세 정보

## 🐛 **Cursor에서 도구가 0개로 보이는 문제**

### 🔍 **문제 원인**

Cursor의 MCP 클라이언트가 초기화 과정을 완전히 완료하지 못하고 있을 가능성

### 🔧 **해결 방법**

#### 1단계: Cursor 완전 재시작

```bash
# Cursor 완전 종료
pkill -f "Cursor"

# 3-5초 대기 후 다시 시작
```

#### 2단계: MCP 설정 확인

현재 설정이 올바른지 확인:

```json
{
  "mcpServers": {
    "game-news-scraper": {
      "command": "/Users/hyuntkim/workspace/my-game-articles/.venv/bin/python",
      "args": ["-m", "src.server"],
      "cwd": "/Users/hyuntkim/workspace/my-game-articles",
      "env": {
        "PYTHONPATH": "/Users/hyuntkim/workspace/my-game-articles",
        "LOG_LEVEL": "DEBUG"
      }
    }
  }
}
```

#### 3단계: 수동 테스트

```bash
# 서버가 정상 동작하는지 확인
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}
{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | /Users/hyuntkim/workspace/my-game-articles/.venv/bin/python -m src.server
```

**예상 결과**: `"tools":[...6개 도구...]` 응답 확인

## 📝 **추가 디버깅 단계**

### MCP 로그 확인

1. Cursor 설정에서 `LOG_LEVEL: "DEBUG"` 설정
2. Cursor 재시작 후 MCP 로그 확인
3. 초기화 과정에서 오류 메시지 찾기

### 대안적 테스트 방법

```bash
# 간단한 initialize + list_tools 테스트
python -c "
import asyncio
import json
from src.server import server, run_server

async def test():
    print('Server ready')

asyncio.run(test())
"
```

## 🎯 **성공 지표**

MCP 서버가 정상 작동하면:

- Cursor에서 `@game-news-scraper` 자동완성 표시
- 6개 도구가 모두 Cursor MCP 패널에 표시
- 예시 명령어 실행 가능:
  ```
  로드나인의 최신 공지사항을 알려주세요
  ```

## 🚨 **문제 지속 시 확인사항**

1. **Python 가상환경 활성화 확인**
2. **MCP 라이브러리 버전 확인**: `pip show mcp`
3. **Cursor 버전 호환성 확인**
4. **시스템 권한 문제 확인**

## 📞 **최종 해결책**

만약 위 방법들이 모두 실패하면:

1. Cursor 설정 파일 완전 삭제 후 재설정
2. MCP 서버를 HTTP 모드로 변경 고려
3. 다른 MCP 클라이언트로 테스트 (Claude Desktop 등)

---

**현재 상태**: MCP 서버는 정상 동작 중 ✅  
**문제**: Cursor 클라이언트 초기화 이슈로 추정 🔍
