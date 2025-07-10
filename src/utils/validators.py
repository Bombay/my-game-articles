"""데이터 검증 및 직렬화 관련 함수들"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import ValidationError

from src.models.game_news import GameNews, GameType, NewsType
from src.models.exceptions import ValidationException

def validate_game_news(data: Dict[str, Any]) -> bool:
    """GameNews 데이터 유효성 검증
    
    Args:
        data: 검증할 데이터 딕셔너리
        
    Returns:
        bool: 유효성 여부
    """
    try:
        GameNews(**data)
        return True
    except ValidationError:
        return False

def validate_game_news_list(data_list: List[Dict[str, Any]]) -> List[bool]:
    """GameNews 리스트 데이터 유효성 검증
    
    Args:
        data_list: 검증할 데이터 리스트
        
    Returns:
        List[bool]: 각 항목의 유효성 여부
    """
    return [validate_game_news(data) for data in data_list]

def create_game_news_from_dict(data: Dict[str, Any]) -> GameNews:
    """딕셔너리에서 GameNews 객체 생성
    
    Args:
        data: 게임 뉴스 데이터
        
    Returns:
        GameNews: 생성된 GameNews 객체
        
    Raises:
        ValidationException: 유효하지 않은 데이터인 경우
    """
    try:
        return GameNews(**data)
    except ValidationError as e:
        raise ValidationException(f"유효하지 않은 게임 뉴스 데이터: {e}")

def serialize_game_news(news: GameNews) -> Dict[str, Any]:
    """GameNews 객체를 딕셔너리로 직렬화
    
    Args:
        news: 직렬화할 GameNews 객체
        
    Returns:
        Dict[str, Any]: 직렬화된 데이터
    """
    return news.dict()

def serialize_game_news_list(news_list: List[GameNews]) -> List[Dict[str, Any]]:
    """GameNews 리스트를 딕셔너리 리스트로 직렬화
    
    Args:
        news_list: 직렬화할 GameNews 리스트
        
    Returns:
        List[Dict[str, Any]]: 직렬화된 데이터 리스트
    """
    return [serialize_game_news(news) for news in news_list]

def game_news_to_json(news: GameNews) -> str:
    """GameNews 객체를 JSON 문자열로 변환
    
    Args:
        news: 변환할 GameNews 객체
        
    Returns:
        str: JSON 문자열
    """
    return news.json()

def game_news_list_to_json(news_list: List[GameNews]) -> str:
    """GameNews 리스트를 JSON 문자열로 변환
    
    Args:
        news_list: 변환할 GameNews 리스트
        
    Returns:
        str: JSON 문자열
    """
    serialized = serialize_game_news_list(news_list)
    return json.dumps(serialized, ensure_ascii=False, indent=2)

def validate_game_type(game: str) -> bool:
    """게임 타입 유효성 검증
    
    Args:
        game: 검증할 게임 타입 문자열
        
    Returns:
        bool: 유효한 게임 타입인지 여부
    """
    try:
        GameType(game)
        return True
    except ValueError:
        return False

def validate_news_type(news_type: str) -> bool:
    """뉴스 타입 유효성 검증
    
    Args:
        news_type: 검증할 뉴스 타입 문자열
        
    Returns:
        bool: 유효한 뉴스 타입인지 여부
    """
    try:
        NewsType(news_type)
        return True
    except ValueError:
        return False

def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
    """필수 필드 존재 여부 검증
    
    Args:
        data: 검증할 데이터
        required_fields: 필수 필드 목록
        
    Returns:
        bool: 모든 필수 필드가 존재하는지 여부
    """
    return all(field in data and data[field] is not None for field in required_fields)

def sanitize_html(text: str) -> str:
    """HTML 태그 및 특수 문자 제거
    
    Args:
        text: 정제할 텍스트
        
    Returns:
        str: 정제된 텍스트
    """
    import re
    
    if not text:
        return ""
    
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    
    # 특수 HTML 엔티티 변환
    html_entities = {
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&#39;': "'",
        '&nbsp;': ' ',
    }
    
    for entity, char in html_entities.items():
        text = text.replace(entity, char)
    
    # 연속된 공백 제거
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def validate_datetime_range(dt: datetime, min_date: Optional[datetime] = None, max_date: Optional[datetime] = None) -> bool:
    """날짜 범위 유효성 검증
    
    Args:
        dt: 검증할 날짜
        min_date: 최소 날짜 (선택적)
        max_date: 최대 날짜 (선택적)
        
    Returns:
        bool: 유효한 날짜 범위인지 여부
    """
    if min_date and dt < min_date:
        return False
    
    if max_date and dt > max_date:
        return False
    
    return True

def normalize_game_news_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """게임 뉴스 데이터 정규화
    
    Args:
        data: 정규화할 데이터
        
    Returns:
        Dict[str, Any]: 정규화된 데이터
    """
    normalized = data.copy()
    
    # 제목 정제
    if 'title' in normalized:
        normalized['title'] = sanitize_html(str(normalized['title']))
    
    # 내용 정제
    if 'content' in normalized and normalized['content']:
        normalized['content'] = sanitize_html(str(normalized['content']))
    
    # 요약 정제
    if 'summary' in normalized and normalized['summary']:
        normalized['summary'] = sanitize_html(str(normalized['summary']))
    
    # 태그 정규화
    if 'tags' in normalized and normalized['tags']:
        if isinstance(normalized['tags'], str):
            normalized['tags'] = [tag.strip() for tag in normalized['tags'].split(',')]
        elif isinstance(normalized['tags'], list):
            normalized['tags'] = [str(tag).strip() for tag in normalized['tags']]
    
    # 조회수 정규화
    if 'view_count' in normalized and normalized['view_count']:
        try:
            normalized['view_count'] = int(normalized['view_count'])
        except (ValueError, TypeError):
            normalized['view_count'] = None
    
    return normalized

class GameNewsValidator:
    """GameNews 데이터 검증 클래스"""
    
    def __init__(self):
        self.errors: List[str] = []
    
    def validate(self, data: Dict[str, Any]) -> bool:
        """종합적인 데이터 검증
        
        Args:
            data: 검증할 데이터
            
        Returns:
            bool: 유효성 여부
        """
        self.errors.clear()
        
        # 필수 필드 검증
        required_fields = ['id', 'title', 'url', 'published_at', 'game', 'category']
        if not validate_required_fields(data, required_fields):
            self.errors.append("필수 필드가 누락되었습니다")
        
        # 게임 타입 검증
        if 'game' in data and not validate_game_type(data['game']):
            self.errors.append(f"유효하지 않은 게임 타입: {data['game']}")
        
        # 뉴스 타입 검증
        if 'category' in data and not validate_news_type(data['category']):
            self.errors.append(f"유효하지 않은 뉴스 타입: {data['category']}")
        
        # Pydantic 검증
        if not validate_game_news(data):
            self.errors.append("Pydantic 검증 실패")
        
        return len(self.errors) == 0
    
    def get_errors(self) -> List[str]:
        """검증 오류 목록 반환
        
        Returns:
            List[str]: 오류 목록
        """
        return self.errors.copy() 