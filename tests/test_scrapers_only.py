"""
스크래퍼 단독 테스트 (MCP 의존성 없음)
"""

import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scrapers.lordnine import LordnineScraper
from src.scrapers.epic_seven import EpicSevenScraper
from src.scrapers.lost_ark import LostArkScraper


async def test_all_scrapers():
    """모든 게임 스크래퍼 테스트"""
    
    print("🚀 게임 스크래퍼 통합 테스트 시작...\n")
    
    # 스크래퍼들 초기화
    scrapers = {
        "로드나인": LordnineScraper(),
        "에픽세븐": EpicSevenScraper(),
        "로스트아크": LostArkScraper()
    }
    
    # 각 게임별 테스트
    for game_name, scraper in scrapers.items():
        print(f"📋 {game_name} 스크래퍼 테스트 시작...")
        
        try:
            # 공지사항 테스트
            print(f"  📢 {game_name} 공지사항 목록 조회...")
            announcements = await scraper.get_announcements()
            if announcements and len(announcements) > 0:
                print(f"    ✅ 공지사항 {len(announcements)}개 조회 성공")
                print(f"    첫 번째: {announcements[0].title}")
            else:
                print(f"    ⚠️ 공지사항 0개")
            
            # 이벤트 테스트
            print(f"  🎉 {game_name} 이벤트 목록 조회...")
            events = await scraper.get_events()
            if events and len(events) > 0:
                print(f"    ✅ 이벤트 {len(events)}개 조회 성공")
                print(f"    첫 번째: {events[0].title}")
            else:
                print(f"    ⚠️ 이벤트 0개")
            
            # 업데이트 테스트
            print(f"  🔄 {game_name} 업데이트 목록 조회...")
            updates = await scraper.get_updates()
            if updates and len(updates) > 0:
                print(f"    ✅ 업데이트 {len(updates)}개 조회 성공")
                print(f"    첫 번째: {updates[0].title}")
            else:
                print(f"    ⚠️ 업데이트 0개")
            
            print(f"  ✅ {game_name} 스크래퍼 테스트 완료\n")
            
        except Exception as e:
            print(f"  ❌ {game_name} 스크래퍼 테스트 실패: {e}\n")
    
    print("🏁 모든 스크래퍼 테스트 완료!")


async def test_specific_scraper(game_name: str):
    """특정 게임 스크래퍼 상세 테스트"""
    
    scrapers = {
        "lordnine": LordnineScraper(),
        "epic_seven": EpicSevenScraper(),
        "lost_ark": LostArkScraper()
    }
    
    if game_name not in scrapers:
        print(f"지원하지 않는 게임: {game_name}")
        return
    
    scraper = scrapers[game_name]
    print(f"🎮 {game_name} 스크래퍼 상세 테스트 시작...\n")
    
    try:
        # 공지사항 목록 및 첫 번째 상세 조회
        print("📢 공지사항 테스트...")
        announcements = await scraper.get_announcements()
        if announcements and len(announcements) > 0:
            print(f"공지사항 {len(announcements)}개 조회 성공")
            print(f"첫 번째 제목: {announcements[0].title}")
            print(f"첫 번째 URL: {announcements[0].url}")
            
            # 첫 번째 공지사항 상세 조회
            detail = await scraper.get_announcement_detail(announcements[0].url)
            if detail:
                print(f"상세 조회 성공: {detail.title[:50]}...")
            print()
        
        # 이벤트 목록 조회
        print("🎉 이벤트 테스트...")
        events = await scraper.get_events()
        if events and len(events) > 0:
            print(f"이벤트 {len(events)}개 조회 성공")
            print(f"첫 번째 제목: {events[0].title}")
            print()
        
        # 업데이트 목록 조회
        print("🔄 업데이트 테스트...")
        updates = await scraper.get_updates()
        if updates and len(updates) > 0:
            print(f"업데이트 {len(updates)}개 조회 성공")
            print(f"첫 번째 제목: {updates[0].title}")
            print()
        
        print(f"✅ {game_name} 스크래퍼 상세 테스트 완료!")
        
    except Exception as e:
        print(f"❌ {game_name} 스크래퍼 상세 테스트 실패: {e}")


if __name__ == "__main__":
    # 통합 테스트 실행
    if len(sys.argv) > 1:
        # 특정 게임 테스트
        game = sys.argv[1]
        asyncio.run(test_specific_scraper(game))
    else:
        # 전체 테스트
        asyncio.run(test_all_scrapers()) 