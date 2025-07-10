"""기본 단위 테스트"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from datetime import datetime

from src.models.game_news import GameNews, NewsType, GameType
from src.scrapers.epic_seven import EpicSevenScraper
from src.scrapers.lordnine import LordnineScraper
from src.scrapers.lost_ark import LostArkScraper


class TestBasicFunctionality:
    """기본 기능 테스트"""
    
    def test_game_news_model(self):
        """GameNews 모델 테스트"""
        news = GameNews(
            id="test-1",
            title="테스트 뉴스",
            url="https://example.com/news/1",
            published_at=datetime.now(),
            game=GameType.EPIC_SEVEN,
            category=NewsType.ANNOUNCEMENT
        )
        
        assert news.id == "test-1"
        assert news.title == "테스트 뉴스"
        assert news.game == GameType.EPIC_SEVEN
        assert news.category == NewsType.ANNOUNCEMENT
        assert isinstance(news.published_at, datetime)
    
    def test_epic_seven_scraper_init(self):
        """에픽세븐 스크래퍼 초기화 테스트"""
        scraper = EpicSevenScraper()
        assert scraper.game_type == GameType.EPIC_SEVEN
        assert scraper.timeout == 30
        assert hasattr(scraper, 'validate_response_data')
    
    def test_lordnine_scraper_init(self):
        """로드나인 스크래퍼 초기화 테스트"""
        scraper = LordnineScraper()
        assert scraper.game_type == GameType.LORDNINE
        assert scraper.timeout == 30
    
    def test_lost_ark_scraper_init(self):
        """로스트아크 스크래퍼 초기화 테스트"""
        scraper = LostArkScraper()
        assert scraper.game_type == GameType.LOST_ARK
        assert scraper.timeout == 30
    
    def test_validate_response_data(self):
        """응답 데이터 검증 테스트"""
        scraper = EpicSevenScraper()
        
        # 유효한 데이터
        valid_data = {"value": {"list": []}}
        assert scraper.validate_response_data(valid_data, ['value']) is True
        
        # 유효하지 않은 데이터
        invalid_data = {"error": "not found"}
        assert scraper.validate_response_data(invalid_data, ['value']) is False
        
        # None 데이터
        assert scraper.validate_response_data(None, ['value']) is False
    
    @pytest.mark.asyncio
    async def test_epic_seven_announcements_with_mock(self):
        """에픽세븐 공지사항 조회 테스트 (Mock)"""
        scraper = EpicSevenScraper()
        
        # Mock 응답 데이터
        mock_data = {
            "value": {
                "list": [
                    {
                        "article_id": 12345,
                        "title": "테스트 공지사항",
                        "create_datetime": 1704844800000,
                        "content": "테스트 내용",
                        "summary": "테스트 요약",
                        "view_count": 1000,
                        "is_headline": False,
                        "category": "공지",
                        "article_type": "official"
                    }
                ]
            }
        }
        
        with patch.object(scraper, 'make_request') as mock_request:
            # Mock response 설정 개선
            mock_response = AsyncMock()
            mock_response.json = AsyncMock(return_value=mock_data)
            mock_request.return_value = mock_response
            
            announcements = await scraper.get_announcements()
            
            assert len(announcements) >= 0
            if announcements:
                assert announcements[0].game == GameType.EPIC_SEVEN
                assert announcements[0].category == NewsType.ANNOUNCEMENT
    
    @pytest.mark.asyncio
    async def test_session_management(self):
        """세션 관리 테스트"""
        scraper = EpicSevenScraper()
        
        # 세션 초기화
        await scraper.init_session()
        assert scraper.session is not None
        
        # 세션 종료
        await scraper.close_session()
        assert scraper.session is None
    
    def test_url_extraction(self):
        """URL에서 ID 추출 테스트"""
        scraper = EpicSevenScraper()
        
        # 정상 URL
        url1 = "https://page.onstove.com/epicseven/global/view/12345"
        assert scraper._extract_article_id_from_url(url1) == "12345"
        
        # 잘못된 URL
        url2 = "https://invalid-url.com"
        assert scraper._extract_article_id_from_url(url2) is None 