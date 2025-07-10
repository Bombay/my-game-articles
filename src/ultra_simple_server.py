#!/usr/bin/env python3

import asyncio
import json
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from typing import Any, Dict, List, Sequence

# 최소한의 서버
app = Server("ultra-simple")


@app.list_tools()
async def list_tools() -> List[Tool]:
    """단순한 6개 툴"""
    return [
        Tool(
            name="tool1",
            description="Tool 1",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="tool2", 
            description="Tool 2",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="tool3",
            description="Tool 3", 
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="tool4",
            description="Tool 4",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="tool5",
            description="Tool 5",
            inputSchema={"type": "object", "properties": {}, "required": []}
        ),
        Tool(
            name="tool6",
            description="Tool 6",
            inputSchema={"type": "object", "properties": {}, "required": []}
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """툴 호출"""
    return [TextContent(type="text", text=f"Called {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        from mcp.server.models import InitializationOptions
        from mcp.types import ServerCapabilities
        await app.run(
            read_stream,
            write_stream, 
            InitializationOptions(
                server_name="ultra-simple",
                server_version="1.0.0",
                capabilities=ServerCapabilities()
            )
        )


if __name__ == "__main__":
    asyncio.run(main()) 