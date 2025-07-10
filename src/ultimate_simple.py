#!/usr/bin/env python3

import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any, Dict, List, Sequence

# 가장 간단한 서버
app = Server("simple")

print("ULTIMATE: 시작", file=sys.stderr)


@app.list_tools()
async def list_tools() -> List[Tool]:
    print("ULTIMATE: list_tools 호출", file=sys.stderr)
    
    return [
        Tool(
            name="test_tool",
            description="테스트 툴",
            inputSchema={"type": "object", "properties": {}, "required": []}
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    print(f"ULTIMATE: 툴 호출 - {name}", file=sys.stderr)
    return [TextContent(type="text", text=f"성공: {name}")]


async def main():
    print("ULTIMATE: main", file=sys.stderr)
    
    async with stdio_server() as (read_stream, write_stream):
        print("ULTIMATE: stdio 연결", file=sys.stderr)
        
        from mcp.server.models import InitializationOptions
        from mcp.types import ServerCapabilities
        
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="simple",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )


if __name__ == "__main__":
    asyncio.run(main()) 