#!/usr/bin/env python3

import asyncio
import sys
import traceback
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any, Dict, List, Sequence

# 디버깅용 서버
app = Server("debug-server")

print("=== DEBUG: 서버 객체 생성됨 ===", file=sys.stderr)


@app.list_tools()
async def list_tools() -> List[Tool]:
    """디버깅용 툴 목록"""
    print("=== DEBUG: list_tools 함수 호출됨 ===", file=sys.stderr)
    
    try:
        tools = [
            Tool(
                name="debug_tool_1",
                description="디버그 툴 1",
                inputSchema={"type": "object", "properties": {}, "required": []}
            ),
            Tool(
                name="debug_tool_2", 
                description="디버그 툴 2",
                inputSchema={"type": "object", "properties": {}, "required": []}
            ),
            Tool(
                name="debug_tool_3",
                description="디버그 툴 3", 
                inputSchema={"type": "object", "properties": {}, "required": []}
            ),
            Tool(
                name="debug_tool_4",
                description="디버그 툴 4",
                inputSchema={"type": "object", "properties": {}, "required": []}
            ),
            Tool(
                name="debug_tool_5",
                description="디버그 툴 5",
                inputSchema={"type": "object", "properties": {}, "required": []}
            ),
            Tool(
                name="debug_tool_6",
                description="디버그 툴 6",
                inputSchema={"type": "object", "properties": {}, "required": []}
            )
        ]
        
        print(f"=== DEBUG: {len(tools)}개 툴 생성됨 ===", file=sys.stderr)
        for tool in tools:
            print(f"=== DEBUG: 툴 - {tool.name}: {tool.description} ===", file=sys.stderr)
        
        return tools
        
    except Exception as e:
        print(f"=== DEBUG ERROR in list_tools: {e} ===", file=sys.stderr)
        print(f"=== DEBUG TRACEBACK: {traceback.format_exc()} ===", file=sys.stderr)
        return []


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """디버깅용 툴 호출"""
    print(f"=== DEBUG: call_tool 호출됨 - {name} ===", file=sys.stderr)
    return [TextContent(type="text", text=f"DEBUG: Called {name}")]


async def main():
    print("=== DEBUG: main 함수 시작 ===", file=sys.stderr)
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            print("=== DEBUG: stdio_server 연결됨 ===", file=sys.stderr)
            
            from mcp.server.models import InitializationOptions
            from mcp.types import ServerCapabilities
            
            init_options = InitializationOptions(
                server_name="debug-server",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
            
            print(f"=== DEBUG: 초기화 옵션 생성됨 - {init_options} ===", file=sys.stderr)
            
            await app.run(read_stream, write_stream, init_options)
            
    except Exception as e:
        print(f"=== DEBUG ERROR in main: {e} ===", file=sys.stderr)
        print(f"=== DEBUG TRACEBACK: {traceback.format_exc()} ===", file=sys.stderr)
        raise


if __name__ == "__main__":
    print("=== DEBUG: 스크립트 시작됨 ===", file=sys.stderr)
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"=== DEBUG ERROR at top level: {e} ===", file=sys.stderr)
        print(f"=== DEBUG TRACEBACK: {traceback.format_exc()} ===", file=sys.stderr) 