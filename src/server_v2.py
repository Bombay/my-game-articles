"""
게임 뉴스 수집 MCP 서버 (간단한 버전)
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, Tool, TextContent
from typing import Any, Dict, List, Sequence

from .config.settings import settings
from .handlers.lordnine import LordnineHandler
from .handlers.epic_seven import EpicSevenHandler
from .handlers.lost_ark import LostArkHandler


# 로깅 설정
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# MCP 서버 생성
app = Server(settings.SERVER_NAME)

# 게임별 핸들러 초기화
handlers = {
    "lordnine": LordnineHandler(),
    "epic_seven": EpicSevenHandler(),
    "lost_ark": LostArkHandler()
}


@app.list_tools()
async def handle_list_tools() -> List[Tool]:
    """사용 가능한 도구 목록 반환"""
    logger.info("도구 목록 요청 받음")
    
    tools = [
        Tool(
            name="get_game_announcements",
            description="지정된 게임의 최신 공지사항 목록을 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": settings.SUPPORTED_GAMES,
                        "description": "게임 이름 (lordnine, epic_seven, lost_ark)"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_announcement_detail",
            description="특정 공지사항의 상세 정보를 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": settings.SUPPORTED_GAMES,
                        "description": "게임 이름 (lordnine, epic_seven, lost_ark)"
                    },
                    "url": {
                        "type": "string",
                        "description": "공지사항 URL"
                    }
                },
                "required": ["game", "url"]
            }
        ),
        Tool(
            name="get_game_events",
            description="지정된 게임의 최신 이벤트 목록을 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": settings.SUPPORTED_GAMES,
                        "description": "게임 이름 (lordnine, epic_seven, lost_ark)"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_event_detail",
            description="특정 이벤트의 상세 정보를 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": settings.SUPPORTED_GAMES,
                        "description": "게임 이름 (lordnine, epic_seven, lost_ark)"
                    },
                    "url": {
                        "type": "string",
                        "description": "이벤트 URL"
                    }
                },
                "required": ["game", "url"]
            }
        ),
        Tool(
            name="get_game_updates",
            description="지정된 게임의 최신 업데이트 목록을 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": settings.SUPPORTED_GAMES,
                        "description": "게임 이름 (lordnine, epic_seven, lost_ark)"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_update_detail",
            description="특정 업데이트의 상세 정보를 가져옵니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": settings.SUPPORTED_GAMES,
                        "description": "게임 이름 (lordnine, epic_seven, lost_ark)"
                    },
                    "url": {
                        "type": "string",
                        "description": "업데이트 URL"
                    }
                },
                "required": ["game", "url"]
            }
        )
    ]
    
    logger.info(f"{len(tools)}개 도구 반환")
    return tools


@app.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """도구 호출 핸들러"""
    try:
        logger.info(f"도구 호출: {name}, 인수: {arguments}")
        
        # 게임 파라미터 확인
        game = arguments.get("game")
        if not game or game not in handlers:
            return [TextContent(
                type="text",
                text=f"지원하지 않는 게임입니다: {game}. 지원 게임: {', '.join(settings.SUPPORTED_GAMES)}"
            )]
        
        handler = handlers[game]
        
        # 도구별 핸들러 호출
        if name == "get_game_announcements":
            return await handler.get_announcements(**arguments)
        elif name == "get_announcement_detail":
            url = arguments.get("url")
            if not url:
                return [TextContent(type="text", text="URL 파라미터가 필요합니다.")]
            return await handler.get_announcement_detail(url, **arguments)
        elif name == "get_game_events":
            return await handler.get_events(**arguments)
        elif name == "get_event_detail":
            url = arguments.get("url")
            if not url:
                return [TextContent(type="text", text="URL 파라미터가 필요합니다.")]
            return await handler.get_event_detail(url, **arguments)
        elif name == "get_game_updates":
            return await handler.get_updates(**arguments)
        elif name == "get_update_detail":
            url = arguments.get("url")
            if not url:
                return [TextContent(type="text", text="URL 파라미터가 필요합니다.")]
            return await handler.get_update_detail(url, **arguments)
        else:
            return [TextContent(type="text", text=f"알 수 없는 도구입니다: {name}")]
    
    except Exception as e:
        logger.error(f"도구 호출 실패: {name}, 오류: {e}")
        return [TextContent(type="text", text=f"오류: {str(e)}")]


async def main():
    """메인 함수"""
    logger.info(f"게임 뉴스 MCP 서버 시작: {settings.SERVER_NAME} v{settings.SERVER_VERSION}")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=settings.SERVER_NAME,
                server_version=settings.SERVER_VERSION,
                capabilities=ServerCapabilities()
            )
        )


if __name__ == "__main__":
    asyncio.run(main()) 