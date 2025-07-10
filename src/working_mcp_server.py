#!/usr/bin/env python3

import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any, Dict, List, Sequence

# 표준 MCP 서버
app = Server("game-news-tools")

print("=== 게임 뉴스 MCP 서버 시작 ===", file=sys.stderr)


@app.list_tools()
async def list_tools() -> List[Tool]:
    """6개 게임 뉴스 툴 목록 반환"""
    print("=== 툴 목록 요청됨 - 6개 툴 반환 ===", file=sys.stderr)
    
    return [
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
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 이름"
                    },
                    "announcement_id": {
                        "type": "string",
                        "description": "공지사항 ID"
                    }
                },
                "required": ["game", "announcement_id"]
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
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 이름"
                    },
                    "event_id": {
                        "type": "string",
                        "description": "이벤트 ID"
                    }
                },
                "required": ["game", "event_id"]
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
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 이름"
                    },
                    "update_id": {
                        "type": "string",
                        "description": "업데이트 ID"
                    }
                },
                "required": ["game", "update_id"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """툴 호출 처리"""
    print(f"=== 툴 호출: {name} with {arguments} ===", file=sys.stderr)
    
    game = arguments.get("game", "unknown")
    
    if name == "get_game_announcements":
        return [TextContent(
            type="text", 
            text=f"✅ {game} 게임의 최신 공지사항 목록입니다.\n\n1. 신규 업데이트 공지\n2. 이벤트 종료 안내\n3. 시스템 점검 안내"
        )]
    
    elif name == "get_announcement_detail":
        announcement_id = arguments.get("announcement_id", "unknown")
        return [TextContent(
            type="text",
            text=f"✅ {game} 게임 공지사항 [{announcement_id}] 상세 정보입니다.\n\n제목: 중요 업데이트 공지\n내용: 게임 시스템이 개선되었습니다.\n날짜: 2025-01-10"
        )]
    
    elif name == "get_game_events":
        return [TextContent(
            type="text",
            text=f"✅ {game} 게임의 진행 중인 이벤트 목록입니다.\n\n1. 신년 특별 이벤트\n2. 레벨업 보상 2배\n3. 한정 아이템 획득 이벤트"
        )]
    
    elif name == "get_event_detail":
        event_id = arguments.get("event_id", "unknown")
        return [TextContent(
            type="text",
            text=f"✅ {game} 게임 이벤트 [{event_id}] 상세 정보입니다.\n\n이벤트명: 신년 특별 이벤트\n기간: 2025-01-01 ~ 2025-01-31\n보상: 레어 아이템 증정"
        )]
    
    elif name == "get_game_updates":
        return [TextContent(
            type="text",
            text=f"✅ {game} 게임의 최근 업데이트 목록입니다.\n\n1. v1.5.0 - 새로운 던전 추가\n2. v1.4.8 - 버그 수정\n3. v1.4.7 - 밸런스 조정"
        )]
    
    elif name == "get_update_detail":
        update_id = arguments.get("update_id", "unknown")
        return [TextContent(
            type="text",
            text=f"✅ {game} 게임 업데이트 [{update_id}] 상세 정보입니다.\n\n버전: v1.5.0\n내용: 새로운 던전과 보스 몬스터가 추가되었습니다.\n날짜: 2025-01-08"
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"❌ 알 수 없는 툴: {name}"
        )]


async def main():
    print("=== MCP 서버 메인 시작 ===", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        print("=== STDIO 연결 완료 ===", file=sys.stderr)
        
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main()) 