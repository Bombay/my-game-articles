#!/usr/bin/env python3
"""
게임 뉴스 수집 MCP 서버 - 메인 진입점
"""

import asyncio
import logging
import sys
import json
from typing import List, Sequence, Any, Dict

# MCP 관련 import
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, Tool, TextContent, ToolsCapability

# 게임 스크래퍼 import
from src.scrapers.lordnine import LordnineScraper
from src.scrapers.epic_seven import EpicSevenScraper
from src.scrapers.lost_ark import LostArkScraper
from src.models.exceptions import ScrapingException

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# 서버 생성
app = Server("game-news-scraper")

# 스크래퍼 인스턴스
scrapers = {
    "lordnine": LordnineScraper(),
    "epic_seven": EpicSevenScraper(),
    "lost_ark": LostArkScraper()
}

@app.list_tools()
async def list_tools() -> List[Tool]:
    """게임 뉴스 수집 도구 목록"""
    logger.info("=== 게임 뉴스 수집 도구 목록 요청됨 ===")
    
    tools = [
        Tool(
            name="get_game_announcements",
            description="게임의 공지사항 목록을 조회합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 종류 (lordnine: 로드나인, epic_seven: 에픽세븐, lost_ark: 로스트아크)"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50,
                        "description": "조회할 공지사항 수 (기본값: 10)"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_announcement_detail",
            description="공지사항의 상세 정보를 조회합니다",
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
            description="게임의 이벤트 목록을 조회합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 종류"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50,
                        "description": "조회할 이벤트 수 (기본값: 10)"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_event_detail",
            description="이벤트의 상세 정보를 조회합니다",
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
            description="게임의 업데이트 목록을 조회합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "game": {
                        "type": "string",
                        "enum": ["lordnine", "epic_seven", "lost_ark"],
                        "description": "게임 종류"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 50,
                        "description": "조회할 업데이트 수 (기본값: 10)"
                    }
                },
                "required": ["game"]
            }
        ),
        Tool(
            name="get_update_detail",
            description="업데이트의 상세 정보를 조회합니다",
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
    
    logger.info(f"=== {len(tools)}개 도구 반환 ===")
    return tools

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """도구 호출 처리"""
    logger.info(f"=== 도구 호출: {name}, 인수: {arguments} ===")
    
    try:
        game = arguments.get("game")
        if game not in scrapers:
            return [TextContent(type="text", text=f"❌ 지원하지 않는 게임입니다: {game}")]
        
        scraper = scrapers[game]
        
        if name == "get_game_announcements":
            return await handle_get_announcements(scraper, arguments)
        elif name == "get_announcement_detail":
            return await handle_get_announcement_detail(scraper, arguments)
        elif name == "get_game_events":
            return await handle_get_events(scraper, arguments)
        elif name == "get_event_detail":
            return await handle_get_event_detail(scraper, arguments)
        elif name == "get_game_updates":
            return await handle_get_updates(scraper, arguments)
        elif name == "get_update_detail":
            return await handle_get_update_detail(scraper, arguments)
        else:
            return [TextContent(type="text", text=f"❌ 알 수 없는 도구: {name}")]
            
    except Exception as e:
        logger.error(f"도구 실행 중 오류: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 오류 발생: {str(e)}")]

async def handle_get_announcements(scraper, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """공지사항 목록 조회 처리"""
    try:
        limit = arguments.get("limit", 10)
        announcements = await scraper.get_announcements()
        
        if not announcements:
            return [TextContent(type="text", text="📋 공지사항이 없습니다.")]
        
        # 제한된 개수만 반환
        limited_announcements = announcements[:limit]
        
        result = f"📢 **{scraper.game_type.value} 공지사항** ({len(limited_announcements)}개)\n\n"
        
        for i, news in enumerate(limited_announcements, 1):
            result += f"**{i}. {news.title}**\n"
            result += f"   📅 {news.published_at.strftime('%Y-%m-%d %H:%M')}\n"
            result += f"   🔗 {news.url}\n"
            if news.tags:
                result += f"   🏷️ {', '.join(news.tags)}\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"공지사항 조회 오류: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 공지사항 조회 중 오류 발생: {str(e)}")]

async def handle_get_announcement_detail(scraper, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """공지사항 상세 조회 처리"""
    try:
        url = arguments.get("url")
        if not url:
            return [TextContent(type="text", text="❌ URL이 필요합니다.")]
        
        detail = await scraper.get_announcement_detail(url)
        
        if not detail:
            return [TextContent(type="text", text="❌ 공지사항 상세 정보를 찾을 수 없습니다.")]
        
        result = f"📢 **{detail.title}**\n\n"
        result += f"📅 **게시일:** {detail.published_at.strftime('%Y-%m-%d %H:%M')}\n"
        result += f"🔗 **URL:** {detail.url}\n"
        if detail.tags:
            result += f"🏷️ **태그:** {', '.join(detail.tags)}\n"
        result += "\n"
        
        if detail.content:
            result += "📝 **내용:**\n"
            result += detail.content[:1000]  # 내용 제한
            if len(detail.content) > 1000:
                result += "...\n\n(내용이 길어서 일부만 표시됩니다)"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"공지사항 상세 조회 오류: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 공지사항 상세 조회 중 오류 발생: {str(e)}")]

async def handle_get_events(scraper, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """이벤트 목록 조회 처리"""
    try:
        limit = arguments.get("limit", 10)
        events = await scraper.get_events()
        
        if not events:
            return [TextContent(type="text", text="🎉 진행 중인 이벤트가 없습니다.")]
        
        limited_events = events[:limit]
        
        result = f"🎉 **{scraper.game_type.value} 이벤트** ({len(limited_events)}개)\n\n"
        
        for i, news in enumerate(limited_events, 1):
            result += f"**{i}. {news.title}**\n"
            result += f"   📅 {news.published_at.strftime('%Y-%m-%d %H:%M')}\n"
            result += f"   🔗 {news.url}\n"
            if news.tags:
                result += f"   🏷️ {', '.join(news.tags)}\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"이벤트 조회 오류: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 이벤트 조회 중 오류 발생: {str(e)}")]

async def handle_get_event_detail(scraper, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """이벤트 상세 조회 처리"""
    try:
        url = arguments.get("url")
        if not url:
            return [TextContent(type="text", text="❌ URL이 필요합니다.")]
        
        detail = await scraper.get_event_detail(url)
        
        if not detail:
            return [TextContent(type="text", text="❌ 이벤트 상세 정보를 찾을 수 없습니다.")]
        
        result = f"🎉 **{detail.title}**\n\n"
        result += f"📅 **게시일:** {detail.published_at.strftime('%Y-%m-%d %H:%M')}\n"
        result += f"🔗 **URL:** {detail.url}\n"
        if detail.tags:
            result += f"🏷️ **태그:** {', '.join(detail.tags)}\n"
        result += "\n"
        
        if detail.content:
            result += "📝 **내용:**\n"
            result += detail.content[:1000]
            if len(detail.content) > 1000:
                result += "...\n\n(내용이 길어서 일부만 표시됩니다)"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"이벤트 상세 조회 오류: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 이벤트 상세 조회 중 오류 발생: {str(e)}")]

async def handle_get_updates(scraper, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """업데이트 목록 조회 처리"""
    try:
        limit = arguments.get("limit", 10)
        updates = await scraper.get_updates()
        
        if not updates:
            return [TextContent(type="text", text="🔄 최근 업데이트가 없습니다.")]
        
        limited_updates = updates[:limit]
        
        result = f"🔄 **{scraper.game_type.value} 업데이트** ({len(limited_updates)}개)\n\n"
        
        for i, news in enumerate(limited_updates, 1):
            result += f"**{i}. {news.title}**\n"
            result += f"   📅 {news.published_at.strftime('%Y-%m-%d %H:%M')}\n"
            result += f"   🔗 {news.url}\n"
            if news.tags:
                result += f"   🏷️ {', '.join(news.tags)}\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"업데이트 조회 오류: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 업데이트 조회 중 오류 발생: {str(e)}")]

async def handle_get_update_detail(scraper, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """업데이트 상세 조회 처리"""
    try:
        url = arguments.get("url")
        if not url:
            return [TextContent(type="text", text="❌ URL이 필요합니다.")]
        
        detail = await scraper.get_update_detail(url)
        
        if not detail:
            return [TextContent(type="text", text="❌ 업데이트 상세 정보를 찾을 수 없습니다.")]
        
        result = f"🔄 **{detail.title}**\n\n"
        result += f"📅 **게시일:** {detail.published_at.strftime('%Y-%m-%d %H:%M')}\n"
        result += f"🔗 **URL:** {detail.url}\n"
        if detail.tags:
            result += f"🏷️ **태그:** {', '.join(detail.tags)}\n"
        result += "\n"
        
        if detail.content:
            result += "📝 **내용:**\n"
            result += detail.content[:1000]
            if len(detail.content) > 1000:
                result += "...\n\n(내용이 길어서 일부만 표시됩니다)"
        
        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"업데이트 상세 조회 오류: {e}", exc_info=True)
        return [TextContent(type="text", text=f"❌ 업데이트 상세 조회 중 오류 발생: {str(e)}")]

async def main():
    logger.info("=== 게임 뉴스 수집 MCP 서버 시작 ===")
    
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("=== STDIO 서버 시작됨 ===")
            
            # 명시적으로 툴 기능 활성화
            capabilities = ServerCapabilities(
                tools=ToolsCapability(listChanged=True)
            )
            
            await app.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="game-news-scraper",
                    server_version="1.0.0",
                    capabilities=capabilities
                )
            )
    except Exception as e:
        logger.error(f"서버 실행 오류: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main()) 