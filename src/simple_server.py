"""
간단한 MCP 서버 (호환성 테스트용)
"""

import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, Tool, TextContent
from typing import Any, Dict, List, Sequence


# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 서버 생성
app = Server("simple-game-news")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """간단한 도구 목록"""
    logger.info("=== 간단한 도구 목록 요청됨 ===")
    
    tools = [
        Tool(
            name="test_lordnine",
            description="로드나인 테스트 도구",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="test_epic_seven", 
            description="에픽세븐 테스트 도구",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="test_lost_ark",
            description="로스트아크 테스트 도구", 
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]
    
    logger.info(f"=== {len(tools)}개 도구 반환 ===")
    return tools


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """도구 호출"""
    logger.info(f"=== 도구 호출: {name} ===")
    
    if name == "test_lordnine":
        return [TextContent(type="text", text="로드나인 테스트 성공!")]
    elif name == "test_epic_seven":
        return [TextContent(type="text", text="에픽세븐 테스트 성공!")]
    elif name == "test_lost_ark":
        return [TextContent(type="text", text="로스트아크 테스트 성공!")]
    else:
        return [TextContent(type="text", text=f"알 수 없는 도구: {name}")]


async def main():
    """메인 실행 함수"""
    logger.info("=== 간단한 MCP 서버 시작 ===")
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="simple-game-news",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )


if __name__ == "__main__":
    asyncio.run(main()) 