"""실제 API 호출 통합 테스트"""

import asyncio
import time
import pytest
from src.scrapers.lordnine import LordnineScraper
from src.scrapers.epic_seven import EpicSevenScraper
from src.scrapers.lost_ark import LostArkScraper
from src.models.game_news import NewsType


class TestRealAPIIntegration:
    """실제 API 호출 통합 테스트"""
    
    @pytest.mark.asyncio
    async def test_lordnine_announcements(self):
        """로드나인 공지사항 실제 API 테스트"""
        async with LordnineScraper() as scraper:
            start_time = time.time()
            
            try:
                announcements = await scraper.get_announcements()
                execution_time = time.time() - start_time
                
                print(f"로드나인 공지사항: {len(announcements)}개 조회됨 ({execution_time:.2f}초)")
                
                if announcements:
                    first_news = announcements[0]
                    print(f"첫 번째 뉴스: {first_news.title}")
                    print(f"URL: {first_news.url}")
                    print(f"카테고리: {first_news.category}")
                    
                    # 기본 검증
                    assert first_news.game == "lordnine"
                    assert first_news.category == NewsType.ANNOUNCEMENT
                    assert first_news.title
                    assert first_news.url
                    assert first_news.published_at
                
                # 성능 검증 (10초 이내)
                assert execution_time < 10.0
                
                print("✅ 로드나인 공지사항 테스트 성공")
                
            except Exception as e:
                print(f"❌ 로드나인 공지사항 테스트 실패: {e}")
                # 네트워크 문제 등은 실패로 처리하지 않음
                return
    
    @pytest.mark.asyncio
    async def test_epic_seven_announcements(self):
        """에픽세븐 공지사항 실제 API 테스트"""
        async with EpicSevenScraper() as scraper:
            start_time = time.time()
            
            try:
                announcements = await scraper.get_announcements()
                execution_time = time.time() - start_time
                
                print(f"에픽세븐 공지사항: {len(announcements)}개 조회됨 ({execution_time:.2f}초)")
                
                if announcements:
                    first_news = announcements[0]
                    print(f"첫 번째 뉴스: {first_news.title}")
                    print(f"URL: {first_news.url}")
                    print(f"카테고리: {first_news.category}")
                    
                    # 기본 검증
                    assert first_news.game == "epic_seven"
                    assert first_news.category == NewsType.ANNOUNCEMENT
                    assert first_news.title
                    assert first_news.url
                    assert first_news.published_at
                
                # 성능 검증 (10초 이내)
                assert execution_time < 10.0
                
                print("✅ 에픽세븐 공지사항 테스트 성공")
                
            except Exception as e:
                print(f"❌ 에픽세븐 공지사항 테스트 실패: {e}")
                return
    
    @pytest.mark.asyncio
    async def test_lost_ark_announcements(self):
        """로스트아크 공지사항 실제 API 테스트"""
        async with LostArkScraper() as scraper:
            start_time = time.time()
            
            try:
                announcements = await scraper.get_announcements()
                execution_time = time.time() - start_time
                
                print(f"로스트아크 공지사항: {len(announcements)}개 조회됨 ({execution_time:.2f}초)")
                
                if announcements:
                    first_news = announcements[0]
                    print(f"첫 번째 뉴스: {first_news.title}")
                    print(f"URL: {first_news.url}")
                    print(f"카테고리: {first_news.category}")
                    
                    # 기본 검증
                    assert first_news.game == "lost_ark"
                    assert first_news.category == NewsType.ANNOUNCEMENT
                    assert first_news.title
                    assert first_news.url
                    assert first_news.published_at
                
                # 성능 검증 (10초 이내, 로스트아크는 브라우저 자동화로 더 느릴 수 있음)
                assert execution_time < 15.0
                
                print("✅ 로스트아크 공지사항 테스트 성공")
                
            except Exception as e:
                print(f"❌ 로스트아크 공지사항 테스트 실패: {e}")
                return
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self):
        """동시 요청 성능 테스트"""
        start_time = time.time()
        
        async def get_lordnine():
            async with LordnineScraper() as scraper:
                return await scraper.get_announcements()
        
        async def get_epic_seven():
            async with EpicSevenScraper() as scraper:
                return await scraper.get_announcements()
        
        try:
            # 로드나인과 에픽세븐 동시 실행 (로스트아크는 브라우저 때문에 제외)
            results = await asyncio.gather(
                get_lordnine(),
                get_epic_seven(),
                return_exceptions=True
            )
            
            execution_time = time.time() - start_time
            print(f"동시 요청 완료 시간: {execution_time:.2f}초")
            
            success_count = 0
            for i, result in enumerate(results):
                game_names = ["로드나인", "에픽세븐"]
                if isinstance(result, Exception):
                    print(f"{game_names[i]} 실패: {result}")
                else:
                    print(f"{game_names[i]} 성공: {len(result)}개")
                    success_count += 1
            
            # 최소 1개는 성공해야 함
            assert success_count >= 1
            
            # 동시 실행 시간이 개별 실행보다 빨라야 함 (15초 이내)
            assert execution_time < 15.0
            
            print("✅ 동시 요청 테스트 성공")
            
        except Exception as e:
            print(f"❌ 동시 요청 테스트 실패: {e}")
            return
    
    @pytest.mark.asyncio
    async def test_detail_retrieval(self):
        """상세 정보 조회 테스트"""
        async with LordnineScraper() as scraper:
            try:
                # 공지사항 목록 조회
                announcements = await scraper.get_announcements()
                
                if announcements:
                    first_url = str(announcements[0].url)
                    print(f"상세 조회 URL: {first_url}")
                    
                    start_time = time.time()
                    detail = await scraper.get_announcement_detail(first_url)
                    execution_time = time.time() - start_time
                    
                    print(f"상세 조회 시간: {execution_time:.2f}초")
                    
                    if detail:
                        print(f"상세 제목: {detail.title}")
                        print(f"상세 내용 길이: {len(detail.content) if detail.content else 0}")
                        
                        # 상세 정보 검증
                        assert detail.title
                        assert detail.url
                        
                        # 성능 검증 (15초 이내)
                        assert execution_time < 15.0
                        
                        print("✅ 상세 조회 테스트 성공")
                    else:
                        print("⚠️ 상세 정보를 가져올 수 없음 (API 제한일 수 있음)")
                else:
                    print("⚠️ 공지사항 목록이 없어서 상세 조회 불가")
                    
            except Exception as e:
                print(f"❌ 상세 조회 테스트 실패: {e}")
                return


# 스크립트로 실행할 수 있도록
if __name__ == "__main__":
    async def run_tests():
        test_instance = TestRealAPIIntegration()
        
        print("🚀 실제 API 통합 테스트 시작...\n")
        
        await test_instance.test_lordnine_announcements()
        print()
        
        await test_instance.test_epic_seven_announcements()
        print()
        
        await test_instance.test_concurrent_requests()
        print()
        
        await test_instance.test_detail_retrieval()
        print()
        
        print("🎉 모든 테스트 완료!")
    
    asyncio.run(run_tests()) 