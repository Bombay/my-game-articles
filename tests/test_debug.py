"""디버깅용 테스트"""

import pytest
from src.scrapers.epic_seven import EpicSevenScraper


def test_validate_response_data_debug():
    """validate_response_data 메서드 디버깅"""
    scraper = EpicSevenScraper()
    
    # 테스트할 데이터
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
    
    print(f"Mock data type: {type(mock_data)}")
    print(f"Mock data keys: {mock_data.keys()}")
    print(f"Mock data: {mock_data}")
    
    # validate_response_data 호출
    result = scraper.validate_response_data(mock_data, ['value'])
    print(f"Validation result: {result}")
    
    # 세부적으로 확인
    print(f"'value' in mock_data: {'value' in mock_data}")
    print(f"isinstance(mock_data, dict): {isinstance(mock_data, dict)}")
    
    # 기본 validate_response_data 함수 직접 테스트
    assert isinstance(mock_data, dict)
    assert 'value' in mock_data
    assert result is True 