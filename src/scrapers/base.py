"""게임 스크래퍼 기본 클래스"""

from abc import ABC, abstractmethod
from typing import List, Optional
import httpx
import asyncio
from datetime import datetime

from src.models.game_news import GameNews, GameType, NewsType
from src.models.exceptions import (
    NetworkException, 
    TimeoutException, 
    ApiException,
    ScrapingException
)
from src.utils.helpers import parse_timestamp, normalize_url, clean_text

class BaseScraper(ABC):
    """게임 스크래퍼 기본 추상 클래스"""
    
    def __init__(self, game_type: GameType, timeout: int = 30):
        """
        Args:
            game_type: 게임 타입
            timeout: 요청 타임아웃 (초)
        """
        self.game_type = game_type
        self.timeout = timeout
        self.session: Optional[httpx.AsyncClient] = None
        
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        await self.init_session()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        await self.close_session()
        
    async def init_session(self):
        """HTTP 세션 초기화"""
        if self.session is None:
            self.session = httpx.AsyncClient(
                timeout=self.timeout,
                headers=self.get_default_headers()
            )
    
    async def close_session(self):
        """HTTP 세션 종료"""
        if self.session:
            await self.session.aclose()
            self.session = None
    
    def get_default_headers(self) -> dict:
        """기본 HTTP 헤더 반환"""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    async def make_request(self, url: str, method: str = 'GET', **kwargs) -> httpx.Response:
        """HTTP 요청 실행
        
        Args:
            url: 요청 URL
            method: HTTP 메서드
            **kwargs: 추가 요청 파라미터
            
        Returns:
            httpx.Response: 응답 객체
            
        Raises:
            NetworkException: 네트워크 오류
            TimeoutException: 타임아웃 오류
            ApiException: API 오류
        """
        if not self.session:
            await self.init_session()
        
        try:
            assert self.session is not None
            response = await self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
            
        except httpx.TimeoutException as e:
            raise TimeoutException(f"요청 타임아웃: {url}", self.timeout) from e
        except httpx.HTTPStatusError as e:
            raise ApiException(
                f"HTTP 오류 {e.response.status_code}: {url}",
                url,
                {"status_code": e.response.status_code}
            ) from e
        except httpx.RequestError as e:
            raise NetworkException(f"네트워크 오류: {url}") from e
    
    def create_game_news(
        self,
        id: str,
        title: str,
        url: str,
        published_at: datetime,
        category: NewsType,
        content: Optional[str] = None,
        summary: Optional[str] = None,
        is_important: bool = False,
        tags: Optional[List[str]] = None,
        view_count: Optional[int] = None
    ) -> GameNews:
        """GameNews 객체 생성
        
        Args:
            id: 뉴스 ID
            title: 제목
            url: URL
            published_at: 발행 일시
            category: 카테고리
            content: 본문 내용
            summary: 요약
            is_important: 중요 여부
            tags: 태그 목록
            view_count: 조회수
            
        Returns:
            GameNews: 생성된 뉴스 객체
        """
        return GameNews(
            id=id,
            title=clean_text(title),
            content=clean_text(content) if content else None,
            summary=clean_text(summary) if summary else None,
            url=normalize_url(url),
            published_at=published_at,
            game=self.game_type,
            category=category,
            is_important=is_important,
            tags=tags or [],
            view_count=view_count
        )
    
    # 추상 메서드들 - 각 게임 스크래퍼에서 구현해야 함
    
    @abstractmethod
    async def get_announcements(self) -> List[GameNews]:
        """공지사항 목록 조회
        
        Returns:
            List[GameNews]: 공지사항 목록
        """
        pass
    
    @abstractmethod
    async def get_announcement_detail(self, url: str) -> Optional[GameNews]:
        """공지사항 상세 조회
        
        Args:
            url: 공지사항 URL
            
        Returns:
            Optional[GameNews]: 공지사항 상세 정보
        """
        pass
    
    @abstractmethod
    async def get_events(self) -> List[GameNews]:
        """이벤트 목록 조회
        
        Returns:
            List[GameNews]: 이벤트 목록
        """
        pass
    
    @abstractmethod
    async def get_event_detail(self, url: str) -> Optional[GameNews]:
        """이벤트 상세 조회
        
        Args:
            url: 이벤트 URL
            
        Returns:
            Optional[GameNews]: 이벤트 상세 정보
        """
        pass
    
    @abstractmethod
    async def get_updates(self) -> List[GameNews]:
        """업데이트 목록 조회
        
        Returns:
            List[GameNews]: 업데이트 목록
        """
        pass
    
    @abstractmethod
    async def get_update_detail(self, url: str) -> Optional[GameNews]:
        """업데이트 상세 조회
        
        Args:
            url: 업데이트 URL
            
        Returns:
            Optional[GameNews]: 업데이트 상세 정보
        """
        pass
    
    # 헬퍼 메서드들
    
    async def retry_request(
        self, 
        url: str, 
        max_retries: int = 3, 
        delay: float = 1.0,
        **kwargs
    ) -> httpx.Response:
        """재시도 기능이 있는 HTTP 요청
        
        Args:
            url: 요청 URL
            max_retries: 최대 재시도 횟수
            delay: 재시도 간격 (초)
            **kwargs: 추가 요청 파라미터
            
        Returns:
            httpx.Response: 응답 객체
        """
        last_exception: Optional[Exception] = None
        
        for attempt in range(max_retries + 1):
            try:
                return await self.make_request(url, **kwargs)
            except (NetworkException, TimeoutException) as e:
                last_exception = e
                if attempt < max_retries:
                    await asyncio.sleep(delay * (2 ** attempt))  # 지수 백오프
                    continue
                raise
        
        if last_exception:
            raise last_exception
        else:
            raise NetworkException(f"재시도 실패: {url}")
    
    def validate_response_data(self, data: dict, required_fields: List[str]) -> bool:
        """응답 데이터 검증
        
        Args:
            data: 검증할 데이터
            required_fields: 필수 필드 목록
            
        Returns:
            bool: 유효성 여부
        """
        if not isinstance(data, dict):
            return False
            
        return all(field in data for field in required_fields) 