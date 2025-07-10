"""
로스트아크 게임 핸들러
"""

import logging
from typing import Sequence
from mcp import types

from .base import BaseHandler
from ..scrapers.lost_ark import LostArkScraper
from ..models.game_news import NewsType

logger = logging.getLogger(__name__)


class LostArkHandler(BaseHandler):
    """로스트아크 게임 핸들러"""
    
    def __init__(self):
        super().__init__("lost_ark")
        self.scraper = LostArkScraper()
    
    async def get_announcements(self, **kwargs) -> Sequence[types.TextContent]:
        """로스트아크 공지사항 목록 가져오기"""
        try:
            logger.info("로스트아크 공지사항 목록 조회 시작")
            news_list = await self.scraper.get_announcements()
            
            if not news_list:
                return self._create_success_response("현재 공지사항이 없습니다.")
            
            # 뉴스 목록을 텍스트로 포맷팅
            result_lines = [f"📢 로스트아크 공지사항 ({len(news_list)}개)\n"]
            
            for i, news in enumerate(news_list, 1):
                result_lines.append(
                    f"{i}. {news.title}\n"
                    f"   🔗 {news.url}\n"
                    f"   📅 {news.published_date}\n"
                )
            
            logger.info(f"로스트아크 공지사항 {len(news_list)}개 조회 완료")
            return self._create_success_response("\n".join(result_lines))
            
        except Exception as e:
            logger.error(f"로스트아크 공지사항 조회 실패: {e}")
            return self._create_error_response(f"공지사항 조회 중 오류가 발생했습니다: {str(e)}")
    
    async def get_announcement_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """로스트아크 공지사항 상세 정보 가져오기"""
        try:
            logger.info(f"로스트아크 공지사항 상세 조회: {url}")
            detail = await self.scraper.get_announcement_detail(url)
            
            if not detail:
                return self._create_error_response("해당 공지사항을 찾을 수 없습니다.")
            
            result = f"📢 로스트아크 공지사항 상세\n\n"
            result += f"제목: {detail.title}\n"
            result += f"URL: {detail.url}\n"
            result += f"작성일: {detail.published_date}\n"
            if detail.summary:
                result += f"요약: {detail.summary}\n"
            if detail.tags:
                result += f"태그: {', '.join(detail.tags)}\n"
            if detail.content:
                result += f"\n내용:\n{detail.content}\n"
            
            logger.info("로스트아크 공지사항 상세 조회 완료")
            return self._create_success_response(result)
            
        except Exception as e:
            logger.error(f"로스트아크 공지사항 상세 조회 실패: {e}")
            return self._create_error_response(f"공지사항 상세 조회 중 오류가 발생했습니다: {str(e)}")
    
    async def get_events(self, **kwargs) -> Sequence[types.TextContent]:
        """로스트아크 이벤트 목록 가져오기"""
        try:
            logger.info("로스트아크 이벤트 목록 조회 시작")
            news_list = await self.scraper.get_events()
            
            if not news_list:
                return self._create_success_response("현재 진행 중인 이벤트가 없습니다.")
            
            # 뉴스 목록을 텍스트로 포맷팅
            result_lines = [f"🎉 로스트아크 이벤트 ({len(news_list)}개)\n"]
            
            for i, news in enumerate(news_list, 1):
                result_lines.append(
                    f"{i}. {news.title}\n"
                    f"   🔗 {news.url}\n"
                    f"   📅 {news.published_date}\n"
                )
            
            logger.info(f"로스트아크 이벤트 {len(news_list)}개 조회 완료")
            return self._create_success_response("\n".join(result_lines))
            
        except Exception as e:
            logger.error(f"로스트아크 이벤트 조회 실패: {e}")
            return self._create_error_response(f"이벤트 조회 중 오류가 발생했습니다: {str(e)}")
    
    async def get_event_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """로스트아크 이벤트 상세 정보 가져오기"""
        try:
            logger.info(f"로스트아크 이벤트 상세 조회: {url}")
            detail = await self.scraper.get_event_detail(url)
            
            if not detail:
                return self._create_error_response("해당 이벤트를 찾을 수 없습니다.")
            
            result = f"🎉 로스트아크 이벤트 상세\n\n"
            result += f"제목: {detail.title}\n"
            result += f"URL: {detail.url}\n"
            result += f"작성일: {detail.published_date}\n"
            if detail.summary:
                result += f"요약: {detail.summary}\n"
            if detail.tags:
                result += f"태그: {', '.join(detail.tags)}\n"
            if detail.content:
                result += f"\n내용:\n{detail.content}\n"
            
            logger.info("로스트아크 이벤트 상세 조회 완료")
            return self._create_success_response(result)
            
        except Exception as e:
            logger.error(f"로스트아크 이벤트 상세 조회 실패: {e}")
            return self._create_error_response(f"이벤트 상세 조회 중 오류가 발생했습니다: {str(e)}")
    
    async def get_updates(self, **kwargs) -> Sequence[types.TextContent]:
        """로스트아크 업데이트 목록 가져오기"""
        try:
            logger.info("로스트아크 업데이트 목록 조회 시작")
            news_list = await self.scraper.get_updates()
            
            if not news_list:
                return self._create_success_response("현재 업데이트가 없습니다.")
            
            # 뉴스 목록을 텍스트로 포맷팅
            result_lines = [f"🔄 로스트아크 업데이트 ({len(news_list)}개)\n"]
            
            for i, news in enumerate(news_list, 1):
                result_lines.append(
                    f"{i}. {news.title}\n"
                    f"   🔗 {news.url}\n"
                    f"   📅 {news.published_date}\n"
                )
            
            logger.info(f"로스트아크 업데이트 {len(news_list)}개 조회 완료")
            return self._create_success_response("\n".join(result_lines))
            
        except Exception as e:
            logger.error(f"로스트아크 업데이트 조회 실패: {e}")
            return self._create_error_response(f"업데이트 조회 중 오류가 발생했습니다: {str(e)}")
    
    async def get_update_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """로스트아크 업데이트 상세 정보 가져오기"""
        try:
            logger.info(f"로스트아크 업데이트 상세 조회: {url}")
            detail = await self.scraper.get_update_detail(url)
            
            if not detail:
                return self._create_error_response("해당 업데이트를 찾을 수 없습니다.")
            
            result = f"🔄 로스트아크 업데이트 상세\n\n"
            result += f"제목: {detail.title}\n"
            result += f"URL: {detail.url}\n"
            result += f"작성일: {detail.published_date}\n"
            if detail.summary:
                result += f"요약: {detail.summary}\n"
            if detail.tags:
                result += f"태그: {', '.join(detail.tags)}\n"
            if detail.content:
                result += f"\n내용:\n{detail.content}\n"
            
            logger.info("로스트아크 업데이트 상세 조회 완료")
            return self._create_success_response(result)
            
        except Exception as e:
            logger.error(f"로스트아크 업데이트 상세 조회 실패: {e}")
            return self._create_error_response(f"업데이트 상세 조회 중 오류가 발생했습니다: {str(e)}") 