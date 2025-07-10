"""
간단하고 확실한 MCP 서버
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, Tool, TextContent
from typing import Any, Dict, List, Sequence

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 서버 생성
app = Server("game-news-working")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """6개 도구 목록 반환"""
    logger.info("=== 도구 목록 요청됨 ===")
    
    tools = [
        Tool(
            name="get_game_announcements",
            description="지정된 게임의 최신 공지사항 목록을 가져옵니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 이름"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_announcement_detail",
            description="특정 공지사항의 상세 정보를 가져옵니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string", "enum": ["lordnine", "epic_seven", "lost_ark"]},
                    "url": {"type": "string", "description": "공지사항 URL"}
                },
                "required": ["game", "url"]
            }
        ),
        Tool(
            name="get_game_events",
            description="지정된 게임의 최신 이벤트 목록을 가져옵니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 이름"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_event_detail",
            description="특정 이벤트의 상세 정보를 가져옵니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string", "enum": ["lordnine", "epic_seven", "lost_ark"]},
                    "url": {"type": "string", "description": "이벤트 URL"}
                },
                "required": ["game", "url"]
            }
        ),
        Tool(
            name="get_game_updates",
            description="지정된 게임의 최신 업데이트 목록을 가져옵니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 이름"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_update_detail",
            description="특정 업데이트의 상세 정보를 가져옵니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string", "enum": ["lordnine", "epic_seven", "lost_ark"]},
                    "url": {"type": "string", "description": "업데이트 URL"}
                },
                "required": ["game", "url"]
            }
        )
    ]
    
    logger.info(f"=== {len(tools)}개 도구 반환됨 ===")
    for tool in tools:
        logger.info(f"도구: {tool.name}")
    
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """도구 호출 처리"""
    logger.info(f"=== 도구 호출: {name}, 인수: {arguments} ===")
    
    # 실제 구현은 나중에 추가하고, 일단 성공 메시지만 반환
    game = arguments.get("game", "unknown")
    
    if "announcement" in name:
        if "detail" in name:
            return [TextContent(type="text", text=f"[{game}] 공지사항 상세 정보 (테스트)")]
        else:
            return [TextContent(type="text", text=f"[{game}] 공지사항 목록 (테스트)")]
    elif "event" in name:
        if "detail" in name:
            return [TextContent(type="text", text=f"[{game}] 이벤트 상세 정보 (테스트)")]
        else:
            return [TextContent(type="text", text=f"[{game}] 이벤트 목록 (테스트)")]
    elif "update" in name:
        if "detail" in name:
            return [TextContent(type="text", text=f"[{game}] 업데이트 상세 정보 (테스트)")]
        else:
            return [TextContent(type="text", text=f"[{game}] 업데이트 목록 (테스트)")]
    else:
        return [TextContent(type="text", text=f"알 수 없는 도구: {name}")]


async def main():
    """메인 실행 함수"""
    logger.info("=== 게임 뉴스 MCP 서버 시작 ===")
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info("=== stdio 서버 연결됨 ===")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="game-news-working",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )


if __name__ == "__main__":
    asyncio.run(main()) 