"""
에픽세븐 게임 핸들러
"""

import json
from typing import Sequence
from mcp import types

from .base import BaseHandler
from src.scrapers.epic_seven import EpicSevenScraper


class EpicSevenHandler(BaseHandler):
    """에픽세븐 게임 핸들러"""
    
    def __init__(self):
        super().__init__("epic_seven")
        self.scraper = EpicSevenScraper()
    
    async def get_announcements(self, **kwargs) -> Sequence[types.TextContent]:
        """에픽세븐 공지사항 목록 가져오기"""
        try:
            news_list = await self.scraper.get_announcements()
            
            if not news_list:
                return self._create_error_response("공지사항을 찾을 수 없습니다")
            
            # 결과를 JSON 형태로 포맷팅
            formatted_news = []
            for news in news_list:
                formatted_news.append({
                    "id": news.id,
                    "title": news.title,
                    "url": str(news.url),
                    "published_date": news.published_at.isoformat() if news.published_at else None,
                    "summary": news.summary,
                    "tags": news.tags,
                    "view_count": news.view_count
                })
            
            return self._create_success_response(
                f"에픽세븐 공지사항 {len(news_list)}개를 가져왔습니다.\n\n" +
                json.dumps(formatted_news, ensure_ascii=False, indent=2)
            )
            
        except Exception as e:
            return self._create_error_response(f"공지사항 조회 중 오류 발생: {str(e)}")
    
    async def get_announcement_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """에픽세븐 공지사항 상세 정보 가져오기"""
        try:
            news_detail = await self.scraper.get_announcement_detail(url)
            
            if not news_detail:
                return self._create_error_response("공지사항 상세 정보를 찾을 수 없습니다")
            
            formatted_detail = {
                "id": news_detail.id,
                "title": news_detail.title,
                "url": str(news_detail.url),
                "published_date": news_detail.published_at.isoformat() if news_detail.published_at else None,
                "summary": news_detail.summary,
                "content": news_detail.content,
                "tags": news_detail.tags,
                "view_count": news_detail.view_count,
                "category": news_detail.category.value if news_detail.category else None
            }
            
            return self._create_success_response(
                f"에픽세븐 공지사항 상세 정보:\n\n" +
                json.dumps(formatted_detail, ensure_ascii=False, indent=2)
            )
            
        except Exception as e:
            return self._create_error_response(f"공지사항 상세 조회 중 오류 발생: {str(e)}")
    
    async def get_events(self, **kwargs) -> Sequence[types.TextContent]:
        """에픽세븐 이벤트 목록 가져오기"""
        try:
            news_list = await self.scraper.get_events()
            
            if not news_list:
                return self._create_error_response("이벤트를 찾을 수 없습니다")
            
            # 결과를 JSON 형태로 포맷팅
            formatted_news = []
            for news in news_list:
                formatted_news.append({
                    "id": news.id,
                    "title": news.title,
                    "url": str(news.url),
                    "published_date": news.published_at.isoformat() if news.published_at else None,
                    "summary": news.summary,
                    "tags": news.tags,
                    "view_count": news.view_count
                })
            
            return self._create_success_response(
                f"에픽세븐 이벤트 {len(news_list)}개를 가져왔습니다.\n\n" +
                json.dumps(formatted_news, ensure_ascii=False, indent=2)
            )
            
        except Exception as e:
            return self._create_error_response(f"이벤트 조회 중 오류 발생: {str(e)}")
    
    async def get_event_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """에픽세븐 이벤트 상세 정보 가져오기"""
        try:
            news_detail = await self.scraper.get_event_detail(url)
            
            if not news_detail:
                return self._create_error_response("이벤트 상세 정보를 찾을 수 없습니다")
            
            formatted_detail = {
                "id": news_detail.id,
                "title": news_detail.title,
                "url": str(news_detail.url),
                "published_date": news_detail.published_at.isoformat() if news_detail.published_at else None,
                "summary": news_detail.summary,
                "content": news_detail.content,
                "tags": news_detail.tags,
                "view_count": news_detail.view_count,
                "category": news_detail.category.value if news_detail.category else None
            }
            
            return self._create_success_response(
                f"에픽세븐 이벤트 상세 정보:\n\n" +
                json.dumps(formatted_detail, ensure_ascii=False, indent=2)
            )
            
        except Exception as e:
            return self._create_error_response(f"이벤트 상세 조회 중 오류 발생: {str(e)}")
    
    async def get_updates(self, **kwargs) -> Sequence[types.TextContent]:
        """에픽세븐 업데이트 목록 가져오기"""
        try:
            news_list = await self.scraper.get_updates()
            
            if not news_list:
                return self._create_error_response("업데이트를 찾을 수 없습니다")
            
            # 결과를 JSON 형태로 포맷팅
            formatted_news = []
            for news in news_list:
                formatted_news.append({
                    "id": news.id,
                    "title": news.title,
                    "url": str(news.url),
                    "published_date": news.published_at.isoformat() if news.published_at else None,
                    "summary": news.summary,
                    "tags": news.tags,
                    "view_count": news.view_count
                })
            
            return self._create_success_response(
                f"에픽세븐 업데이트 {len(news_list)}개를 가져왔습니다.\n\n" +
                json.dumps(formatted_news, ensure_ascii=False, indent=2)
            )
            
        except Exception as e:
            return self._create_error_response(f"업데이트 조회 중 오류 발생: {str(e)}")
    
    async def get_update_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """에픽세븐 업데이트 상세 정보 가져오기"""
        try:
            news_detail = await self.scraper.get_update_detail(url)
            
            if not news_detail:
                return self._create_error_response("업데이트 상세 정보를 찾을 수 없습니다")
            
            formatted_detail = {
                "id": news_detail.id,
                "title": news_detail.title,
                "url": str(news_detail.url),
                "published_date": news_detail.published_at.isoformat() if news_detail.published_at else None,
                "summary": news_detail.summary,
                "content": news_detail.content,
                "tags": news_detail.tags,
                "view_count": news_detail.view_count,
                "category": news_detail.category.value if news_detail.category else None
            }
            
            return self._create_success_response(
                f"에픽세븐 업데이트 상세 정보:\n\n" +
                json.dumps(formatted_detail, ensure_ascii=False, indent=2)
            )
            
        except Exception as e:
            return self._create_error_response(f"업데이트 상세 조회 중 오류 발생: {str(e)}") 