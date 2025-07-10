"""
MCP 서버 통합 테스트
"""

import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.handlers.lordnine import LordnineHandler
from src.handlers.epic_seven import EpicSevenHandler
from src.handlers.lost_ark import LostArkHandler


async def test_all_handlers():
    """모든 게임 핸들러 통합 테스트"""
    
    print("🚀 MCP 서버 통합 테스트 시작...\n")
    
    # 핸들러 초기화
    handlers = {
        "로드나인": LordnineHandler(),
        "에픽세븐": EpicSevenHandler(), 
        "로스트아크": LostArkHandler()
    }
    
    # 각 게임별 테스트
    for game_name, handler in handlers.items():
        print(f"📋 {game_name} 핸들러 테스트 시작...")
        
        try:
            # 공지사항 테스트
            print(f"  📢 {game_name} 공지사항 목록 조회...")
            announcements = await handler.get_announcements()
            if announcements and len(announcements) > 0:
                text_content = announcements[0].text
                if "오류" not in text_content:
                    print(f"    ✅ 공지사항 조회 성공")
                else:
                    print(f"    ❌ 공지사항 조회 실패: {text_content}")
            
            # 이벤트 테스트
            print(f"  🎉 {game_name} 이벤트 목록 조회...")
            events = await handler.get_events()
            if events and len(events) > 0:
                text_content = events[0].text
                if "오류" not in text_content:
                    print(f"    ✅ 이벤트 조회 성공")
                else:
                    print(f"    ❌ 이벤트 조회 실패: {text_content}")
            
            # 업데이트 테스트
            print(f"  🔄 {game_name} 업데이트 목록 조회...")
            updates = await handler.get_updates()
            if updates and len(updates) > 0:
                text_content = updates[0].text
                if "오류" not in text_content:
                    print(f"    ✅ 업데이트 조회 성공")
                else:
                    print(f"    ❌ 업데이트 조회 실패: {text_content}")
            
            print(f"  ✅ {game_name} 핸들러 테스트 완료\n")
            
        except Exception as e:
            print(f"  ❌ {game_name} 핸들러 테스트 실패: {e}\n")
    
    print("🏁 모든 핸들러 테스트 완료!")


async def test_specific_game(game_name: str):
    """특정 게임 핸들러 상세 테스트"""
    
    handlers = {
        "lordnine": LordnineHandler(),
        "epic_seven": EpicSevenHandler(),
        "lost_ark": LostArkHandler()
    }
    
    if game_name not in handlers:
        print(f"지원하지 않는 게임: {game_name}")
        return
    
    handler = handlers[game_name]
    print(f"🎮 {game_name} 상세 테스트 시작...\n")
    
    try:
        # 공지사항 목록 및 첫 번째 상세 조회
        print("📢 공지사항 테스트...")
        announcements = await handler.get_announcements()
        if announcements:
            print(f"공지사항 조회 결과:\n{announcements[0].text[:200]}...\n")
        
        # 이벤트 목록 조회
        print("🎉 이벤트 테스트...")
        events = await handler.get_events()
        if events:
            print(f"이벤트 조회 결과:\n{events[0].text[:200]}...\n")
        
        # 업데이트 목록 조회
        print("🔄 업데이트 테스트...")
        updates = await handler.get_updates()
        if updates:
            print(f"업데이트 조회 결과:\n{updates[0].text[:200]}...\n")
        
        print(f"✅ {game_name} 상세 테스트 완료!")
        
    except Exception as e:
        print(f"❌ {game_name} 상세 테스트 실패: {e}")


if __name__ == "__main__":
    # 통합 테스트 실행
    if len(sys.argv) > 1:
        # 특정 게임 테스트
        game = sys.argv[1]
        asyncio.run(test_specific_game(game))
    else:
        # 전체 테스트
        asyncio.run(test_all_handlers()) 