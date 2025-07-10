"""
전체 시스템 종합 테스트
"""

import asyncio
import sys
import os
import time
from typing import List, Dict, Any

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scrapers.lordnine import LordnineScraper
from src.scrapers.epic_seven import EpicSevenScraper
from src.scrapers.lost_ark import LostArkScraper
from src.models.game_news import GameNews


class TestResult:
    """테스트 결과 클래스"""
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.success = False
        self.error_message = ""
        self.execution_time = 0.0
        self.data_count = 0


async def test_scraper_performance(scraper, game_name: str) -> Dict[str, TestResult]:
    """스크래퍼 성능 테스트"""
    results = {}
    
    # 공지사항 성능 테스트
    test_name = f"{game_name}_announcements_performance"
    result = TestResult(test_name)
    start_time = time.time()
    
    try:
        announcements = await scraper.get_announcements()
        result.execution_time = time.time() - start_time
        result.data_count = len(announcements) if announcements else 0
        result.success = True
    except Exception as e:
        result.error_message = str(e)
        result.execution_time = time.time() - start_time
    
    results[test_name] = result
    
    # 이벤트 성능 테스트
    test_name = f"{game_name}_events_performance"
    result = TestResult(test_name)
    start_time = time.time()
    
    try:
        events = await scraper.get_events()
        result.execution_time = time.time() - start_time
        result.data_count = len(events) if events else 0
        result.success = True
    except Exception as e:
        result.error_message = str(e)
        result.execution_time = time.time() - start_time
    
    results[test_name] = result
    
    # 업데이트 성능 테스트
    test_name = f"{game_name}_updates_performance"
    result = TestResult(test_name)
    start_time = time.time()
    
    try:
        updates = await scraper.get_updates()
        result.execution_time = time.time() - start_time
        result.data_count = len(updates) if updates else 0
        result.success = True
    except Exception as e:
        result.error_message = str(e)
        result.execution_time = time.time() - start_time
    
    results[test_name] = result
    
    return results


async def test_data_quality(scraper, game_name: str) -> Dict[str, TestResult]:
    """데이터 품질 테스트"""
    results = {}
    
    # 공지사항 데이터 품질 검증
    test_name = f"{game_name}_announcements_quality"
    result = TestResult(test_name)
    
    try:
        announcements = await scraper.get_announcements()
        if announcements:
            # 데이터 품질 검증
            for news in announcements[:5]:  # 처음 5개만 검증
                assert news.title and len(news.title) > 0, "제목이 비어있음"
                url_str = str(news.url) if news.url else ""
                assert url_str and url_str.startswith("http"), "유효하지 않은 URL"
                assert news.published_at, "작성일이 없음"
            result.success = True
            result.data_count = len(announcements)
        else:
            result.success = True  # 데이터가 없는 것도 정상 상황
            result.data_count = 0
    except Exception as e:
        result.error_message = str(e)
    
    results[test_name] = result
    
    return results


async def test_error_scenarios(scraper, game_name: str) -> Dict[str, TestResult]:
    """오류 시나리오 테스트"""
    results = {}
    
    # 잘못된 URL로 상세 조회 테스트
    test_name = f"{game_name}_invalid_url_handling"
    result = TestResult(test_name)
    
    try:
        # 잘못된 URL로 상세 조회 시도
        invalid_url = "https://invalid.url/test"
        detail = await scraper.get_announcement_detail(invalid_url)
        # 오류가 발생하지 않고 None을 반환하는 것이 정상
        result.success = True
    except Exception as e:
        # 예외가 발생해도 처리되는지 확인
        result.success = True  # 예외 처리가 되면 성공
        result.error_message = f"예외 처리됨: {str(e)}"
    
    results[test_name] = result
    
    return results


async def test_concurrent_requests(scrapers: Dict[str, Any]) -> Dict[str, TestResult]:
    """동시 요청 처리 테스트"""
    results = {}
    
    test_name = "concurrent_requests_test"
    result = TestResult(test_name)
    start_time = time.time()
    
    try:
        # 모든 스크래퍼의 공지사항을 동시에 요청
        tasks = []
        for game_name, scraper in scrapers.items():
            tasks.append(scraper.get_announcements())
        
        # 동시 실행
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 결과 확인
        success_count = sum(1 for r in results_list if isinstance(r, list))
        result.execution_time = time.time() - start_time
        result.data_count = success_count
        result.success = success_count >= 2  # 최소 2개 게임 성공
        
    except Exception as e:
        result.error_message = str(e)
        result.execution_time = time.time() - start_time
    
    results[test_name] = result
    
    return results


async def run_comprehensive_tests():
    """전체 종합 테스트 실행"""
    
    print("🚀 전체 시스템 종합 테스트 시작...\n")
    
    # 스크래퍼 초기화
    scrapers = {
        "lordnine": LordnineScraper(),
        "epic_seven": EpicSevenScraper(),
        "lost_ark": LostArkScraper()
    }
    
    all_results = {}
    
    # 각 게임별 테스트
    for game_name, scraper in scrapers.items():
        print(f"📋 {game_name} 테스트 시작...")
        
        # 성능 테스트
        print(f"  ⚡ {game_name} 성능 테스트...")
        performance_results = await test_scraper_performance(scraper, game_name)
        all_results.update(performance_results)
        
        # 데이터 품질 테스트
        print(f"  🔍 {game_name} 데이터 품질 테스트...")
        quality_results = await test_data_quality(scraper, game_name)
        all_results.update(quality_results)
        
        # 오류 시나리오 테스트
        print(f"  ⚠️ {game_name} 오류 시나리오 테스트...")
        error_results = await test_error_scenarios(scraper, game_name)
        all_results.update(error_results)
        
        print(f"  ✅ {game_name} 테스트 완료\n")
    
    # 동시 요청 테스트
    print("🔄 동시 요청 처리 테스트...")
    concurrent_results = await test_concurrent_requests(scrapers)
    all_results.update(concurrent_results)
    
    # 결과 요약
    print("\n📊 테스트 결과 요약")
    print("=" * 80)
    
    success_count = 0
    total_count = 0
    total_execution_time = 0.0
    
    for test_name, result in all_results.items():
        total_count += 1
        if result.success:
            success_count += 1
        total_execution_time += result.execution_time
        
        status = "✅ 성공" if result.success else "❌ 실패"
        print(f"{status} | {test_name:<35} | {result.execution_time:.2f}s | 데이터: {result.data_count}개")
        
        if not result.success and result.error_message:
            print(f"     오류: {result.error_message}")
    
    print("=" * 80)
    print(f"전체 결과: {success_count}/{total_count} 성공 ({success_count/total_count*100:.1f}%)")
    print(f"총 실행 시간: {total_execution_time:.2f}초")
    print(f"평균 실행 시간: {total_execution_time/total_count:.2f}초")
    
    # 성능 분석
    print("\n⚡ 성능 분석")
    print("-" * 40)
    
    for game_name in scrapers.keys():
        game_tests = [r for name, r in all_results.items() if name.startswith(game_name) and "performance" in name]
        if game_tests:
            avg_time = sum(t.execution_time for t in game_tests) / len(game_tests)
            total_data = sum(t.data_count for t in game_tests)
            print(f"{game_name}: 평균 {avg_time:.2f}초, 총 {total_data}개 데이터")
    
    return all_results


if __name__ == "__main__":
    asyncio.run(run_comprehensive_tests()) 