"""
게임 뉴스 MCP 서버 설정
"""
import os
from typing import Optional


class Settings:
    """애플리케이션 설정 클래스"""
    
    # 서버 설정
    SERVER_NAME: str = "game-news-mcp"
    SERVER_VERSION: str = "1.0.0"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # 캐싱 설정
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))  # 5분
    ENABLE_CACHE: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    
    # 성능 설정
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))
    
    # HTTP 클라이언트 설정
    USER_AGENT: str = os.getenv(
        "USER_AGENT", 
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    
    # 게임별 설정
    SUPPORTED_GAMES = ["lordnine", "epic_seven", "lost_ark"]
    
    # API 엔드포인트 설정
    LORDNINE_API_BASE = "https://api.onstove.com"
    EPIC_SEVEN_API_BASE = "https://api.onstove.com/cwms/v3.0"
    LOST_ARK_BASE_URL = "https://lostark.game.onstove.com"


# 전역 설정 인스턴스
settings = Settings() 