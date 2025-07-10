"""테스트용 공통 설정 및 fixture"""

import pytest
from unittest.mock import AsyncMock
from src.scrapers.lordnine import LordnineScraper
from src.scrapers.epic_seven import EpicSevenScraper
from src.scrapers.lost_ark import LostArkScraper


@pytest.fixture
def lordnine_scraper():
    """로드나인 스크래퍼 fixture"""
    return LordnineScraper()


@pytest.fixture
def epic_seven_scraper():
    """에픽세븐 스크래퍼 fixture"""
    return EpicSevenScraper()


@pytest.fixture
def lost_ark_scraper():
    """로스트아크 스크래퍼 fixture"""
    return LostArkScraper()


@pytest.fixture
def all_scrapers():
    """모든 스크래퍼 fixture"""
    return {
        "lordnine": LordnineScraper(),
        "epic_seven": EpicSevenScraper(),
        "lost_ark": LostArkScraper()
    } 