import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class ServerSettings(BaseModel):
    name: str = "game-news-mcp"
    version: str = "1.0.0"
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


class ScrapingSettings(BaseModel):
    request_timeout: int = 30
    max_retries: int = 3
    retry_delay: int = 1
    cache_enabled: bool = True
    cache_ttl: int = 300


class BrowserSettings(BaseModel):
    headless: bool = True
    timeout: int = 10000


class AppSettings(BaseModel):
    server: ServerSettings = ServerSettings()
    scraping: ScrapingSettings = ScrapingSettings()
    browser: BrowserSettings = BrowserSettings()
    
    fallback_enabled: bool = True
    error_notification: bool = False

    @classmethod
    def from_env(cls) -> "AppSettings":
        return cls(
            server=ServerSettings(
                name=os.getenv("MCP_SERVER_NAME", "game-news-mcp"),
                version=os.getenv("MCP_SERVER_VERSION", "1.0.0"),
                log_level=os.getenv("LOG_LEVEL", "INFO"),
                log_format=os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            ),
            scraping=ScrapingSettings(
                request_timeout=int(os.getenv("REQUEST_TIMEOUT", "30")),
                max_retries=int(os.getenv("MAX_RETRIES", "3")),
                retry_delay=int(os.getenv("RETRY_DELAY", "1")),
                cache_enabled=os.getenv("CACHE_ENABLED", "true").lower() == "true",
                cache_ttl=int(os.getenv("CACHE_TTL", "300"))
            ),
            browser=BrowserSettings(
                headless=os.getenv("BROWSER_HEADLESS", "true").lower() == "true",
                timeout=int(os.getenv("BROWSER_TIMEOUT", "10000"))
            ),
            fallback_enabled=os.getenv("FALLBACK_ENABLED", "true").lower() == "true",
            error_notification=os.getenv("ERROR_NOTIFICATION", "false").lower() == "true"
        )


settings = AppSettings.from_env()