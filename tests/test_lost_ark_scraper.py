"""로스트아크 스크래퍼 테스트"""

import pytest
import asyncio
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock

# Playwright 모킹을 위한 import
try:
    from src.scrapers.lost_ark import LostArkScraper
    from src.models.game_news import GameNews, NewsType, GameType
    from src.models.exceptions import ScrapingException, TimeoutException
    playwright_available = True
except ImportError:
    playwright_available = False


@pytest.mark.skipif(not playwright_available, reason="Playwright not available")
class TestLostArkScraper:
    """로스트아크 스크래퍼 테스트"""
    
    @pytest.fixture
    def scraper(self):
        """스크래퍼 인스턴스 생성"""
        return LostArkScraper()
    
    @pytest.fixture
    def mock_page(self):
        """모킹된 Playwright 페이지"""
        page_mock = AsyncMock()
        
        # 모킹된 요소들
        element_mock = AsyncMock()
        element_mock.inner_text.return_value = "[공지] 로스트아크 정기 점검 안내"
        element_mock.get_attribute.return_value = "/News/Notice/View/1234"
        
        date_element_mock = AsyncMock()
        date_element_mock.inner_text.return_value = "2024.01.09"
        
        content_element_mock = AsyncMock()
        content_element_mock.inner_text.return_value = "정기 점검이 실시됩니다. 상세한 내용은 다음과 같습니다..."
        
        # 페이지 메서드 설정
        page_mock.goto = AsyncMock()
        page_mock.wait_for_timeout = AsyncMock()
        page_mock.query_selector_all.return_value = [element_mock]
        page_mock.query_selector.side_effect = lambda selector: {
            '.date': date_element_mock,
            '.view-content': content_element_mock,
            '.view-title': element_mock
        }.get(selector)
        page_mock.close = AsyncMock()
        page_mock.set_viewport_size = AsyncMock()
        page_mock.set_extra_http_headers = AsyncMock()
        
        return page_mock
    
    @pytest.fixture
    def mock_browser(self, mock_page):
        """모킹된 Playwright 브라우저"""
        browser_mock = AsyncMock()
        browser_mock.new_page.return_value = mock_page
        browser_mock.close = AsyncMock()
        return browser_mock
    
    @pytest.fixture
    def mock_playwright(self, mock_browser):
        """모킹된 Playwright"""
        playwright_mock = AsyncMock()
        playwright_mock.chromium.launch.return_value = mock_browser
        playwright_mock.stop = AsyncMock()
        return playwright_mock
    
    @pytest.mark.asyncio
    async def test_init_browser(self, scraper, mock_playwright):
        """브라우저 초기화 테스트"""
        with patch('src.scrapers.lost_ark.async_playwright') as playwright_patch:
            playwright_instance = AsyncMock()
            playwright_instance.start.return_value = mock_playwright
            playwright_patch.return_value = playwright_instance
            
            await scraper.init_browser()
            
            assert scraper.playwright is not None
            assert scraper.browser is not None
            mock_playwright.chromium.launch.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_announcements(self, scraper, mock_playwright, mock_browser, mock_page):
        """공지사항 목록 조회 테스트"""
        with patch('src.scrapers.lost_ark.async_playwright') as playwright_patch:
            playwright_instance = AsyncMock()
            playwright_instance.start.return_value = mock_playwright
            playwright_patch.return_value = playwright_instance
            
            async with scraper:
                announcements = await scraper.get_announcements()
                
                assert len(announcements) > 0
                assert all(isinstance(news, GameNews) for news in announcements)
                assert announcements[0].game == GameType.LOST_ARK
                assert announcements[0].category == NewsType.ANNOUNCEMENT
                mock_page.goto.assert_called()
    
    @pytest.mark.asyncio
    async def test_get_events(self, scraper, mock_playwright, mock_browser, mock_page):
        """이벤트 목록 조회 테스트"""
        with patch('src.scrapers.lost_ark.async_playwright') as playwright_patch:
            playwright_instance = AsyncMock()
            playwright_instance.start.return_value = mock_playwright
            playwright_patch.return_value = playwright_instance
            
            async with scraper:
                events = await scraper.get_events()
                
                assert len(events) > 0
                assert all(news.category == NewsType.EVENT for news in events)
    
    @pytest.mark.asyncio
    async def test_get_updates(self, scraper, mock_playwright, mock_browser, mock_page):
        """업데이트 목록 조회 테스트"""
        with patch('src.scrapers.lost_ark.async_playwright') as playwright_patch:
            playwright_instance = AsyncMock()
            playwright_instance.start.return_value = mock_playwright
            playwright_patch.return_value = playwright_instance
            
            async with scraper:
                updates = await scraper.get_updates()
                
                assert len(updates) > 0
                assert all(news.category == NewsType.UPDATE for news in updates)
    
    @pytest.mark.asyncio
    async def test_get_announcement_detail(self, scraper, mock_playwright, mock_browser, mock_page):
        """공지사항 상세 조회 테스트"""
        test_url = "https://lostark.game.onstove.com/News/Notice/View/1234"
        
        with patch('src.scrapers.lost_ark.async_playwright') as playwright_patch:
            playwright_instance = AsyncMock()
            playwright_instance.start.return_value = mock_playwright
            playwright_patch.return_value = playwright_instance
            
            async with scraper:
                detail = await scraper.get_announcement_detail(test_url)
                
                assert detail is not None
                assert detail.category == NewsType.ANNOUNCEMENT
                assert detail.content is not None
                mock_page.goto.assert_called()
    
    def test_extract_id_from_url(self, scraper):
        """URL에서 ID 추출 테스트"""
        test_urls = [
            "https://lostark.game.onstove.com/News/Notice/View/1234",
            "https://lostark.game.onstove.com/News/Event/detail/5678",
            "https://example.com?id=9999",
            "https://invalid-url.com"
        ]
        
        assert scraper._extract_id_from_url(test_urls[0]) == "1234"
        assert scraper._extract_id_from_url(test_urls[1]) == "5678"
        assert scraper._extract_id_from_url(test_urls[2]) == "9999"
        assert scraper._extract_id_from_url(test_urls[3]) is None
    
    def test_is_important_news(self, scraper):
        """중요도 판단 테스트"""
        test_cases = [
            # 중요한 뉴스
            "[긴급] 서버 점검 안내",
            "중요 업데이트 공지",
            "정기 점검 안내",
            "신규 이벤트 출시",
            # 중요하지 않은 뉴스
            "일반 게시글",
            "커뮤니티 소식",
        ]
        
        assert scraper._is_important_news(test_cases[0]) is True  # 긴급
        assert scraper._is_important_news(test_cases[1]) is True  # 중요, 업데이트
        assert scraper._is_important_news(test_cases[2]) is True  # 점검
        assert scraper._is_important_news(test_cases[3]) is True  # 이벤트, 출시
        assert scraper._is_important_news(test_cases[4]) is False  # 일반
        assert scraper._is_important_news(test_cases[5]) is False  # 일반
    
    def test_is_maintenance_notice(self, scraper):
        """점검 공지 판단 테스트"""
        test_cases = [
            # 점검 공지
            "정기 점검 안내",
            "긴급 서버점검 실시",
            "시스템 maintenance 안내",
            # 일반 공지
            "이벤트 안내",
            "업데이트 소식",
        ]
        
        assert scraper._is_maintenance_notice(test_cases[0]) is True
        assert scraper._is_maintenance_notice(test_cases[1]) is True
        assert scraper._is_maintenance_notice(test_cases[2]) is True
        assert scraper._is_maintenance_notice(test_cases[3]) is False
        assert scraper._is_maintenance_notice(test_cases[4]) is False
    
    def test_extract_tags_from_title(self, scraper):
        """제목에서 태그 추출 테스트"""
        test_cases = [
            "[공지] 정기 점검 안내 - 업데이트 포함",
            "신규 이벤트 출시 안내",
            "[패치] 버전 업데이트",
        ]
        
        tags1 = scraper._extract_tags_from_title(test_cases[0])
        assert "공지" in tags1
        assert "점검" in tags1 or "maintenance" in tags1
        assert "업데이트" in tags1 or "update" in tags1
        
        tags2 = scraper._extract_tags_from_title(test_cases[1])
        assert "이벤트" in tags2 or "event" in tags2
        
        tags3 = scraper._extract_tags_from_title(test_cases[2])
        assert "패치" in tags3 or "patch" in tags3
        assert "업데이트" in tags3 or "update" in tags3
    
    @pytest.mark.asyncio
    async def test_timeout_handling(self, scraper):
        """타임아웃 처리 테스트"""
        scraper.timeout = 1  # 1초로 설정
        
        with patch('src.scrapers.lost_ark.async_playwright'):
            with patch.object(scraper, 'create_page') as mock_create_page:
                mock_page = AsyncMock()
                mock_page.goto.side_effect = Exception("timeout")
                mock_page.close = AsyncMock()
                mock_create_page.return_value = mock_page
                
                with pytest.raises((ScrapingException, TimeoutException)):
                    await scraper.get_announcements()
    
    @pytest.mark.asyncio
    async def test_context_manager(self, scraper, mock_playwright):
        """컨텍스트 매니저 테스트"""
        with patch('src.scrapers.lost_ark.async_playwright') as playwright_patch:
            playwright_instance = AsyncMock()
            playwright_instance.start.return_value = mock_playwright
            playwright_patch.return_value = playwright_instance
            
            async with scraper:
                assert scraper.browser is not None
            
            # 컨텍스트 종료 후 브라우저가 정리되었는지 확인
            mock_playwright.stop.assert_called_once()


if __name__ == "__main__":
    # 간단한 실행 테스트 (실제 웹사이트 접근)
    async def test_run():
        print("로스트아크 스크래퍼 테스트 시작...")
        
        try:
            scraper = LostArkScraper(timeout=15)  # 타임아웃 15초
            
            async with scraper:
                print("브라우저 초기화 완료")
                
                # 공지사항 테스트
                try:
                    announcements = await scraper.get_announcements()
                    print(f"공지사항 {len(announcements)}개 조회 성공")
                    
                    if announcements:
                        print(f"첫 번째 공지: {announcements[0].title}")
                        
                        # 상세 정보 테스트
                        detail = await scraper.get_announcement_detail(announcements[0].url)
                        print(f"상세 정보 조회 {'성공' if detail else '실패'}")
                        
                except Exception as e:
                    print(f"공지사항 조회 실패: {e}")
                
                # 이벤트 테스트
                try:
                    events = await scraper.get_events()
                    print(f"이벤트 {len(events)}개 조회 성공")
                except Exception as e:
                    print(f"이벤트 조회 실패: {e}")
                
                # 업데이트 테스트
                try:
                    updates = await scraper.get_updates()
                    print(f"업데이트 {len(updates)}개 조회 성공")
                except Exception as e:
                    print(f"업데이트 조회 실패: {e}")
                
                print("✅ 모든 테스트 완료")
                
        except Exception as e:
            print(f"❌ 테스트 실패: {e}")
            import traceback
            traceback.print_exc()
    
    # 테스트 실행
    if playwright_available:
        asyncio.run(test_run())
    else:
        print("Playwright를 사용할 수 없습니다. 실제 테스트를 건너뜁니다.") 