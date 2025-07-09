import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence
from mcp.server import Server
from mcp.server.session import ServerSession
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    TextContent,
    Tool,
)
from pydantic import BaseModel
from .config.settings import settings
from .handlers.lordnine import LordNineHandler
from .handlers.epic_seven import EpicSevenHandler
from .handlers.lost_ark import LostArkHandler


class GameNewsServer:
    def __init__(self):
        self.server = Server(settings.server.name)
        self.setup_logging()
        self.setup_game_handlers()
        self.setup_handlers()
        self.setup_tools()
    
    def setup_logging(self):
        logging.basicConfig(
            level=getattr(logging, settings.server.log_level),
            format=settings.server.log_format
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting {settings.server.name} v{settings.server.version}")
    
    def setup_game_handlers(self):
        self.handlers = {
            "lordnine": LordNineHandler(),
            "epic_seven": EpicSevenHandler(),
            "lost_ark": LostArkHandler()
        }
        self.logger.info("Game handlers initialized")
    
    def setup_handlers(self):
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="get_game_announcements",
                    description="게임 공지사항 리스트를 가져옵니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "game": {
                                "type": "string",
                                "enum": ["lordnine", "epic_seven", "lost_ark"],
                                "description": "게임 종류 (lordnine, epic_seven, lost_ark)"
                            }
                        },
                        "required": ["game"]
                    }
                ),
                Tool(
                    name="get_announcement_detail",
                    description="공지사항의 상세 내용을 가져옵니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "game": {
                                "type": "string",
                                "enum": ["lordnine", "epic_seven", "lost_ark"],
                                "description": "게임 종류"
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
                    description="게임 이벤트 리스트를 가져옵니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "game": {
                                "type": "string",
                                "enum": ["lordnine", "epic_seven", "lost_ark"],
                                "description": "게임 종류"
                            }
                        },
                        "required": ["game"]
                    }
                ),
                Tool(
                    name="get_event_detail",
                    description="이벤트의 상세 내용을 가져옵니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "game": {
                                "type": "string",
                                "enum": ["lordnine", "epic_seven", "lost_ark"],
                                "description": "게임 종류"
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
                    description="게임 업데이트 리스트를 가져옵니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "game": {
                                "type": "string",
                                "enum": ["lordnine", "epic_seven", "lost_ark"],
                                "description": "게임 종류"
                            }
                        },
                        "required": ["game"]
                    }
                ),
                Tool(
                    name="get_update_detail",
                    description="업데이트의 상세 내용을 가져옵니다",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "game": {
                                "type": "string",
                                "enum": ["lordnine", "epic_seven", "lost_ark"],
                                "description": "게임 종류"
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
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
            try:
                self.logger.info(f"Tool called: {name} with arguments: {arguments}")
                
                if name == "get_game_announcements":
                    return await self.get_game_announcements(arguments)
                elif name == "get_announcement_detail":
                    return await self.get_announcement_detail(arguments)
                elif name == "get_game_events":
                    return await self.get_game_events(arguments)
                elif name == "get_event_detail":
                    return await self.get_event_detail(arguments)
                elif name == "get_game_updates":
                    return await self.get_game_updates(arguments)
                elif name == "get_update_detail":
                    return await self.get_update_detail(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
            
            except Exception as e:
                self.logger.error(f"Error in tool {name}: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]
    
    def setup_tools(self):
        self.logger.info("All tools registered successfully")
    
    async def get_game_announcements(self, arguments: Dict[str, Any]) -> list[TextContent]:
        try:
            game = arguments.get("game")
            if game not in self.handlers:
                raise ValueError(f"지원하지 않는 게임입니다: {game}")
            
            handler = self.handlers[game]
            data = await handler.get_announcements()
            return handler.format_response(data)
        except Exception as e:
            return await self.handlers.get(game, self.handlers["lordnine"]).handle_error(e, "공지사항 리스트 조회")
    
    async def get_announcement_detail(self, arguments: Dict[str, Any]) -> list[TextContent]:
        try:
            game = arguments.get("game")
            url = arguments.get("url")
            
            if game not in self.handlers:
                raise ValueError(f"지원하지 않는 게임입니다: {game}")
            
            handler = self.handlers[game]
            data = await handler.get_announcement_detail(url)
            return handler.format_response(data)
        except Exception as e:
            return await self.handlers.get(game, self.handlers["lordnine"]).handle_error(e, "공지사항 상세 조회")
    
    async def get_game_events(self, arguments: Dict[str, Any]) -> list[TextContent]:
        try:
            game = arguments.get("game")
            
            if game not in self.handlers:
                raise ValueError(f"지원하지 않는 게임입니다: {game}")
            
            handler = self.handlers[game]
            data = await handler.get_events()
            return handler.format_response(data)
        except Exception as e:
            return await self.handlers.get(game, self.handlers["lordnine"]).handle_error(e, "이벤트 리스트 조회")
    
    async def get_event_detail(self, arguments: Dict[str, Any]) -> list[TextContent]:
        try:
            game = arguments.get("game")
            url = arguments.get("url")
            
            if game not in self.handlers:
                raise ValueError(f"지원하지 않는 게임입니다: {game}")
            
            handler = self.handlers[game]
            data = await handler.get_event_detail(url)
            return handler.format_response(data)
        except Exception as e:
            return await self.handlers.get(game, self.handlers["lordnine"]).handle_error(e, "이벤트 상세 조회")
    
    async def get_game_updates(self, arguments: Dict[str, Any]) -> list[TextContent]:
        try:
            game = arguments.get("game")
            
            if game not in self.handlers:
                raise ValueError(f"지원하지 않는 게임입니다: {game}")
            
            handler = self.handlers[game]
            data = await handler.get_updates()
            return handler.format_response(data)
        except Exception as e:
            return await self.handlers.get(game, self.handlers["lordnine"]).handle_error(e, "업데이트 리스트 조회")
    
    async def get_update_detail(self, arguments: Dict[str, Any]) -> list[TextContent]:
        try:
            game = arguments.get("game")
            url = arguments.get("url")
            
            if game not in self.handlers:
                raise ValueError(f"지원하지 않는 게임입니다: {game}")
            
            handler = self.handlers[game]
            data = await handler.get_update_detail(url)
            return handler.format_response(data)
        except Exception as e:
            return await self.handlers.get(game, self.handlers["lordnine"]).handle_error(e, "업데이트 상세 조회")

    async def run(self):
        try:
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}")
            raise


async def main():
    server = GameNewsServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())