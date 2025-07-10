"""에픽세븐 스크래퍼 테스트"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, patch

from src.scrapers.epic_seven import EpicSevenScraper
from src.models.game_news import GameNews, NewsType, GameType
from src.models.exceptions import ScrapingException


class TestEpicSevenScraper:
    """에픽세븐 스크래퍼 테스트"""
    
    @pytest.fixture
    def scraper(self):
        """스크래퍼 인스턴스 생성"""
        return EpicSevenScraper()
    
    @pytest.fixture
    def mock_api_response(self):
        """모킹된 API 응답"""
        return {
            "value": {
                "list": [
                    {
                        "article_id": 12345,
                        "title": "[공지] 에픽세븐 정기 점검 안내",
                        "create_datetime": 1704844800000,  # 2024-01-10 00:00:00
                        "content": "정기 점검이 실시됩니다.",
                        "summary": "정기 점검 안내입니다.",
                        "view_count": 15000,
                        "is_headline": True,
                        "category": "공지",
                        "article_type": "official"
                    },
                    {
                        "article_id": 12346,
                        "title": "🎉 신규 영웅 출시 이벤트",
                        "create_datetime": 1704758400000,  # 2024-01-09 00:00:00
                        "content": "신규 영웅 출시 이벤트가 시작됩니다.",
                        "summary": "신규 영웅 이벤트",
                        "view_count": 8000,
                        "is_headline": False,
                        "category": "이벤트",
                        "article_type": "event"
                    }
                ]
            }
        }
    
    @pytest.fixture
    def mock_detail_response(self):
        """모킹된 상세 API 응답"""
        return {
            "value": {
                "article_id": 12345,
                "title": "[공지] 에픽세븐 정기 점검 안내",
                "create_datetime": 1704844800000,
                "content": "정기 점검이 실시됩니다. 상세한 내용은 다음과 같습니다...",
                "summary": "정기 점검 안내입니다.",
                "view_count": 15000,
                "is_headline": True,
                "category": "공지",
                "article_type": "official"
            }
        }
    
    @pytest.mark.asyncio
    async def test_get_announcements(self, scraper, mock_api_response):
        """공지사항 목록 조회 테스트"""
        with patch.object(scraper, 'make_request') as mock_request:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_api_response
            mock_request.return_value = mock_response
            
            announcements = await scraper.get_announcements()
            
            assert len(announcements) == 2
            assert all(isinstance(news, GameNews) for news in announcements)
            assert announcements[0].game == GameType.EPIC_SEVEN
            assert announcements[0].category == NewsType.ANNOUNCEMENT
            assert "📌" in announcements[0].title  # 중요도 이모지
            assert "🔥" in announcements[0].title  # 조회수 이모지
            assert "📢" in announcements[0].title  # 공지사항 이모지
    
    @pytest.mark.asyncio
    async def test_get_events(self, scraper, mock_api_response):
        """이벤트 목록 조회 테스트"""
        with patch.object(scraper, 'make_request') as mock_request:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_api_response
            mock_request.return_value = mock_response
            
            events = await scraper.get_events()
            
            assert len(events) == 2
            assert all(news.category == NewsType.EVENT for news in events)
            assert "🎉" in events[0].title  # 이벤트 이모지
    
    @pytest.mark.asyncio
    async def test_get_updates(self, scraper, mock_api_response):
        """업데이트 목록 조회 테스트"""
        with patch.object(scraper, 'make_request') as mock_request:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_api_response
            mock_request.return_value = mock_response
            
            updates = await scraper.get_updates()
            
            assert len(updates) == 2
            assert all(news.category == NewsType.UPDATE for news in updates)
            assert "🔄" in updates[0].title  # 업데이트 이모지
    
    @pytest.mark.asyncio
    async def test_get_announcement_detail(self, scraper, mock_detail_response):
        """공지사항 상세 조회 테스트"""
        test_url = "https://page.onstove.com/epicseven/global/view/12345"
        
        with patch.object(scraper, 'make_request') as mock_request:
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_detail_response
            mock_request.return_value = mock_response
            
            detail = await scraper.get_announcement_detail(test_url)
            
            assert detail is not None
            assert detail.id == "12345"
            assert detail.category == NewsType.ANNOUNCEMENT
            assert detail.content is not None
            assert len(detail.content) > len(detail.summary)
    
    @pytest.mark.asyncio
    async def test_get_detail_fallback(self, scraper, mock_api_response):
        """상세 정보 조회 실패 시 fallback 테스트"""
        test_url = "https://page.onstove.com/epicseven/global/view/12345"
        
        with patch.object(scraper, 'make_request') as mock_request:
            # 첫 번째 호출(상세 API)은 실패, 두 번째 호출(목록 API)은 성공
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_api_response
            mock_request.side_effect = [Exception("API 오류"), mock_response]
            
            detail = await scraper.get_announcement_detail(test_url)
            
            assert detail is not None
            assert detail.id == "12345"
            assert detail.content == detail.summary  # fallback에서는 summary를 content로 사용
    
    def test_extract_article_id_from_url(self, scraper):
        """URL에서 article_id 추출 테스트"""
        test_urls = [
            "https://page.onstove.com/epicseven/global/view/12345",
            "https://page.onstove.com/epicseven/global/view/67890",
            "https://invalid-url.com"
        ]
        
        assert scraper._extract_article_id_from_url(test_urls[0]) == "12345"
        assert scraper._extract_article_id_from_url(test_urls[1]) == "67890"
        assert scraper._extract_article_id_from_url(test_urls[2]) is None
    
    def test_is_important_article(self, scraper):
        """중요도 판단 테스트"""
        test_cases = [
            # 중요한 게시글
            {"title": "긴급 점검 안내", "is_headline": False, "view_count": 5000},
            {"title": "일반 공지", "is_headline": True, "view_count": 1000},
            {"title": "인기 이벤트", "is_headline": False, "view_count": 15000},
            # 중요하지 않은 게시글
            {"title": "일반 게시글", "is_headline": False, "view_count": 100},
        ]
        
        assert scraper._is_important_article(test_cases[0]) is True  # 긴급 키워드
        assert scraper._is_important_article(test_cases[1]) is True  # 고정 게시물
        assert scraper._is_important_article(test_cases[2]) is True  # 높은 조회수
        assert scraper._is_important_article(test_cases[3]) is False  # 일반 게시글
    
    def test_extract_tags(self, scraper):
        """태그 추출 테스트"""
        test_article = {
            "title": "[공지] 정기 점검 안내 - 업데이트 포함",
            "category": "공지사항",
            "article_type": "official"
        }
        
        tags = scraper._extract_tags(test_article)
        
        assert "공지" in tags
        assert "점검" in tags
        assert "업데이트" in tags
        assert "공지사항" in tags
        assert "official" in tags
    
    def test_decorate_title(self, scraper):
        """제목 장식 테스트"""
        test_cases = [
            # 중요한 공지사항 (높은 조회수)
            {
                "title": "정기 점검 안내",
                "category": NewsType.ANNOUNCEMENT,
                "is_important": True,
                "view_count": 15000
            },
            # 일반 이벤트
            {
                "title": "신규 영웅 출시",
                "category": NewsType.EVENT,
                "is_important": False,
                "view_count": 5000
            },
            # 업데이트
            {
                "title": "버전 업데이트",
                "category": NewsType.UPDATE,
                "is_important": False,
                "view_count": 3000
            }
        ]
        
        decorated1 = scraper._decorate_title(**test_cases[0])
        assert "📌" in decorated1  # 중요도
        assert "🔥" in decorated1  # 높은 조회수
        assert "📢" in decorated1  # 공지사항
        
        decorated2 = scraper._decorate_title(**test_cases[1])
        assert "📌" not in decorated2  # 중요하지 않음
        assert "🔥" not in decorated2  # 조회수 낮음
        assert "🎉" in decorated2  # 이벤트
        
        decorated3 = scraper._decorate_title(**test_cases[2])
        assert "🔄" in decorated3  # 업데이트
    
    @pytest.mark.asyncio
    async def test_error_handling(self, scraper):
        """에러 처리 테스트"""
        with patch.object(scraper, 'make_request') as mock_request:
            mock_request.side_effect = Exception("네트워크 오류")
            
            with pytest.raises(ScrapingException):
                await scraper.get_announcements()
    
    @pytest.mark.asyncio
    async def test_invalid_response_format(self, scraper):
        """잘못된 응답 형식 테스트"""
        invalid_response = {"error": "Invalid request"}
        
        with patch.object(scraper, 'make_request') as mock_request:
            mock_response = AsyncMock()
            mock_response.json.return_value = invalid_response
            mock_request.return_value = mock_response
            
            with pytest.raises(ScrapingException):
                await scraper.get_announcements()


if __name__ == "__main__":
    # 간단한 실행 테스트
    async def test_run():
        scraper = EpicSevenScraper()
        try:
            async with scraper:
                print("에픽세븐 스크래퍼 테스트 시작...")
                
                # 공지사항 테스트
                announcements = await scraper.get_announcements()
                print(f"공지사항 {len(announcements)}개 조회 성공")
                
                # 이벤트 테스트
                events = await scraper.get_events()
                print(f"이벤트 {len(events)}개 조회 성공")
                
                # 업데이트 테스트
                updates = await scraper.get_updates()
                print(f"업데이트 {len(updates)}개 조회 성공")
                
                # 상세 정보 테스트
                if announcements:
                    first_url = announcements[0].url
                    print(f"첫 번째 공지사항 URL: {first_url}")
                    print(f"URL 타입: {type(first_url)}")
                    article_id = scraper._extract_article_id_from_url(str(first_url))
                    print(f"추출된 article_id: {article_id}")
                    
                    try:
                        detail = await scraper.get_announcement_detail(str(first_url))
                        print(f"상세 정보 조회 {'성공' if detail else '실패'}")
                    except Exception as e:
                        print(f"상세 정보 조회 오류: {e}")
                        print(f"오류 타입: {type(e)}")
                
                print("✅ 모든 테스트 완료")
                
        except Exception as e:
            print(f"❌ 테스트 실패: {e}")
    
    # 테스트 실행
    asyncio.run(test_run()) 