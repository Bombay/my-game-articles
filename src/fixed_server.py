#!/usr/bin/env python3
"""
Cursor MCP 호환 서버 - 웹 검색 결과 기반 수정
"""

import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any, Dict, List, Sequence

# 서버 생성 - 간단한 이름
app = Server("game_news")

print("=== FIXED: 서버 시작됨 ===", file=sys.stderr)


@app.list_tools()
async def list_tools() -> List[Tool]:
    """6개 툴 반환 - 언더스코어 사용"""
    print("=== FIXED: list_tools 호출됨 ===", file=sys.stderr)
    
    tools = [
        Tool(
            name="get_game_announcements",  # 대시 없음
            description="게임 공지사항 목록 조회",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"]
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_announcement_detail",  # 대시 없음  
            description="공지사항 상세 정보 조회",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string", "enum": ["lordnine", "epic_seven", "lost_ark"]},
                    "url": {"type": "string"}
                },
                "required": ["game", "url"]
            }
        ),
        Tool(
            name="get_game_events",  # 대시 없음
            description="게임 이벤트 목록 조회", 
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string", 
                        "enum": ["lordnine", "epic_seven", "lost_ark"]
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_event_detail",  # 대시 없음
            description="이벤트 상세 정보 조회",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string", "enum": ["lordnine", "epic_seven", "lost_ark"]},
                    "url": {"type": "string"}
                },
                "required": ["game", "url"]
            }
        ),
        Tool(
            name="get_game_updates",  # 대시 없음
            description="게임 업데이트 목록 조회",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"]
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_update_detail",  # 대시 없음
            description="업데이트 상세 정보 조회",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {"type": "string", "enum": ["lordnine", "epic_seven", "lost_ark"]},
                    "url": {"type": "string"}
                },
                "required": ["game", "url"]
            }
        )
    ]
    
    print(f"=== FIXED: {len(tools)}개 툴 반환 ===", file=sys.stderr)
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """툴 호출 처리"""
    print(f"=== FIXED: 툴 호출 - {name} ===", file=sys.stderr)
    
    game = arguments.get("game", "unknown")
    return [TextContent(
        type="text", 
        text=f"✅ {name} 실행됨 (게임: {game}) - 테스트 성공!"
    )]


async def main():
    print("=== FIXED: main 시작 ===", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        print("=== FIXED: stdio 연결됨 ===", file=sys.stderr)
        
        from mcp.server.models import InitializationOptions
        from mcp.types import ServerCapabilities
        
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="game_news",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )


if __name__ == "__main__":
    print("=== FIXED: 스크립트 실행 ===", file=sys.stderr)
    asyncio.run(main()) 