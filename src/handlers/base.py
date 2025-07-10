"""
기본 핸들러 클래스
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Sequence
from mcp import types


class BaseHandler(ABC):
    """모든 게임 핸들러의 기본 클래스"""
    
    def __init__(self, game_name: str):
        self.game_name = game_name
    
    @abstractmethod
    async def get_announcements(self, **kwargs) -> Sequence[types.TextContent]:
        """공지사항 목록 가져오기"""
        pass
    
    @abstractmethod
    async def get_announcement_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """공지사항 상세 정보 가져오기"""
        pass
    
    @abstractmethod
    async def get_events(self, **kwargs) -> Sequence[types.TextContent]:
        """이벤트 목록 가져오기"""
        pass
    
    @abstractmethod
    async def get_event_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """이벤트 상세 정보 가져오기"""
        pass
    
    @abstractmethod
    async def get_updates(self, **kwargs) -> Sequence[types.TextContent]:
        """업데이트 목록 가져오기"""
        pass
    
    @abstractmethod
    async def get_update_detail(self, url: str, **kwargs) -> Sequence[types.TextContent]:
        """업데이트 상세 정보 가져오기"""
        pass
    
    def _create_error_response(self, error_message: str) -> Sequence[types.TextContent]:
        """에러 응답 생성"""
        return [
            types.TextContent(
                type="text",
                text=f"오류: {error_message}"
            )
        ]
    
    def _create_success_response(self, data: str) -> Sequence[types.TextContent]:
        """성공 응답 생성"""
        return [
            types.TextContent(
                type="text",
                text=data
            )
        ] 