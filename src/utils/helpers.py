"""공통 유틸리티 함수들"""

import re
import hashlib
from datetime import datetime, timezone
from typing import Optional, Union, List
from urllib.parse import urlparse, urljoin
from src.models.exceptions import InvalidUrlException

def parse_timestamp(timestamp: Union[int, str, datetime]) -> datetime:
    """다양한 형식의 타임스탬프를 datetime 객체로 변환
    
    Args:
        timestamp: UNIX 타임스탬프(초/밀리초), ISO 문자열, 또는 datetime 객체
        
    Returns:
        datetime: UTC 기준 datetime 객체
        
    Raises:
        ValueError: 변환할 수 없는 형식인 경우
    """
    if isinstance(timestamp, datetime):
        return timestamp.replace(tzinfo=timezone.utc) if timestamp.tzinfo is None else timestamp
    
    if isinstance(timestamp, str):
        # ISO 형식 문자열 파싱
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt
        except ValueError:
            # 숫자 문자열일 수 있음
            try:
                timestamp = int(timestamp)
            except ValueError:
                raise ValueError(f"지원하지 않는 날짜 형식입니다: {timestamp}")
    
    if isinstance(timestamp, int):
        # UNIX 타임스탬프 처리
        # 밀리초 단위인지 확인 (13자리 이상)
        if timestamp > 10**10:
            timestamp_float = timestamp / 1000
        else:
            timestamp_float = float(timestamp)
        
        return datetime.fromtimestamp(timestamp_float, tz=timezone.utc)
    
    raise ValueError(f"지원하지 않는 타임스탬프 형식입니다: {type(timestamp)}")

def validate_url(url: str) -> bool:
    """URL 유효성 검증
    
    Args:
        url: 검증할 URL
        
    Returns:
        bool: 유효한 URL인지 여부
    """
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc])
    except Exception:
        return False

def normalize_url(url: str, base_url: Optional[str] = None) -> str:
    """URL 정규화
    
    Args:
        url: 정규화할 URL
        base_url: 상대 URL인 경우 기준이 될 베이스 URL
        
    Returns:
        str: 정규화된 절대 URL
        
    Raises:
        InvalidUrlException: 유효하지 않은 URL인 경우
    """
    if not url:
        raise InvalidUrlException(url)
    
    # 상대 URL인 경우 절대 URL로 변환
    if base_url and not url.startswith(('http://', 'https://')):
        url = urljoin(base_url, url)
    
    if not validate_url(url):
        raise InvalidUrlException(url)
    
    return url

def extract_article_id(url: str) -> Optional[str]:
    """URL에서 게시글 ID 추출
    
    Args:
        url: 게시글 URL
        
    Returns:
        Optional[str]: 추출된 게시글 ID, 없으면 None
    """
    # 다양한 패턴의 게시글 ID 추출
    patterns = [
        r'/view/(\d+)',
        r'/article/(\d+)',
        r'article_id=(\d+)',
        r'id=(\d+)',
        r'/(\d+)$',
        r'/(\d+)/',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def clean_text(text: str) -> str:
    """텍스트 정제
    
    Args:
        text: 정제할 텍스트
        
    Returns:
        str: 정제된 텍스트
    """
    if not text:
        return ""
    
    # HTML 태그 제거
    text = re.sub(r'<[^>]+>', '', text)
    
    # 연속된 공백 제거
    text = re.sub(r'\s+', ' ', text)
    
    # 앞뒤 공백 제거
    text = text.strip()
    
    return text

def generate_news_id(title: str, url: str, published_at: datetime) -> str:
    """뉴스 고유 ID 생성
    
    Args:
        title: 뉴스 제목
        url: 뉴스 URL
        published_at: 발행 일시
        
    Returns:
        str: 고유 ID (해시값)
    """
    # URL에서 게시글 ID 추출 시도
    article_id = extract_article_id(url)
    if article_id:
        return article_id
    
    # 제목, URL, 발행일시를 조합하여 해시 생성
    content = f"{title}|{url}|{published_at.isoformat()}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]

def is_important_news(title: str, keywords: Optional[List[str]] = None) -> bool:
    """중요 뉴스 여부 판단
    
    Args:
        title: 뉴스 제목
        keywords: 중요 키워드 목록 (기본값: 내장 키워드)
        
    Returns:
        bool: 중요 뉴스 여부
    """
    if not keywords:
        keywords = [
            '긴급', '중요', '필독', '공지', '점검', '업데이트', '패치',
            '이벤트', '보상', '버그', '수정', '신규', '추가', '변경'
        ]
    
    title_lower = title.lower()
    
    # 키워드 매칭
    for keyword in keywords:
        if keyword.lower() in title_lower:
            return True
    
    # 특수 문자 패턴 (📌, ⚠️, 🔥 등)
    if re.search(r'[📌⚠️🔥❗️‼️]', title):
        return True
    
    return False

def extract_tags_from_title(title: str) -> List[str]:
    """제목에서 태그 추출
    
    Args:
        title: 뉴스 제목
        
    Returns:
        List[str]: 추출된 태그 목록
    """
    tags = []
    
    # 대괄호 안의 태그 추출 [태그]
    bracket_tags = re.findall(r'\[([^\]]+)\]', title)
    tags.extend(bracket_tags)
    
    # 키워드 기반 태그 추출
    keyword_tags = {
        '점검': ['점검', 'maintenance'],
        '업데이트': ['업데이트', 'update', '패치', 'patch'],
        '이벤트': ['이벤트', 'event'],
        '공지': ['공지', 'notice', 'announcement'],
        '버그': ['버그', 'bug', '수정', 'fix'],
        '신규': ['신규', 'new', '추가', 'add'],
    }
    
    title_lower = title.lower()
    for tag, keywords in keyword_tags.items():
        if any(keyword in title_lower for keyword in keywords):
            tags.append(tag)
    
    return list(set(tags))  # 중복 제거

def format_view_count(count: Optional[int]) -> str:
    """조회수 포맷팅
    
    Args:
        count: 조회수
        
    Returns:
        str: 포맷된 조회수 문자열
    """
    if count is None:
        return "0"
    
    if count >= 1000000:
        return f"{count/1000000:.1f}M"
    elif count >= 1000:
        return f"{count/1000:.1f}K"
    else:
        return str(count)

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """텍스트 자르기
    
    Args:
        text: 자를 텍스트
        max_length: 최대 길이
        suffix: 자른 경우 추가할 접미사
        
    Returns:
        str: 자른 텍스트
    """
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix 