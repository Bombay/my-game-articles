"""게임 뉴스 수집 관련 예외 클래스들"""
from typing import Optional

class GameNewsException(Exception):
    """게임 뉴스 관련 기본 예외 클래스"""
    pass

class ScrapingException(GameNewsException):
    """스크래핑 관련 예외"""
    def __init__(self, message: str, url: Optional[str] = None, status_code: Optional[int] = None):
        super().__init__(message)
        self.url = url
        self.status_code = status_code
        
    def __str__(self):
        base_msg = super().__str__()
        if self.url:
            base_msg += f" (URL: {self.url})"
        if self.status_code:
            base_msg += f" (Status: {self.status_code})"
        return base_msg

class NetworkException(ScrapingException):
    """네트워크 관련 예외"""
    pass

class ParseException(ScrapingException):
    """데이터 파싱 관련 예외"""
    pass

class ValidationException(GameNewsException):
    """데이터 검증 관련 예외"""
    pass

class UnsupportedGameException(GameNewsException):
    """지원하지 않는 게임 관련 예외"""
    def __init__(self, game: str):
        super().__init__(f"지원하지 않는 게임입니다: {game}")
        self.game = game

class ApiException(GameNewsException):
    """API 관련 예외"""
    def __init__(self, message: str, api_endpoint: Optional[str] = None, response_data: Optional[dict] = None):
        super().__init__(message)
        self.api_endpoint = api_endpoint
        self.response_data = response_data

class TimeoutException(NetworkException):
    """타임아웃 관련 예외"""
    def __init__(self, message: str, timeout_seconds: Optional[int] = None):
        super().__init__(message)
        self.timeout_seconds = timeout_seconds

class RateLimitException(NetworkException):
    """요청 제한 관련 예외"""
    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after

class ContentNotFoundException(ScrapingException):
    """콘텐츠를 찾을 수 없는 경우의 예외"""
    pass

class InvalidUrlException(ValidationException):
    """유효하지 않은 URL 관련 예외"""
    def __init__(self, url: str):
        super().__init__(f"유효하지 않은 URL입니다: {url}")
        self.url = url 