from pydantic import BaseModel, HttpUrl, Field, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum

class NewsType(str, Enum):
    """뉴스 카테고리 타입"""
    ANNOUNCEMENT = "announcement"
    EVENT = "event"
    UPDATE = "update"

class GameType(str, Enum):
    """지원하는 게임 타입"""
    LORDNINE = "lordnine"
    EPIC_SEVEN = "epic_seven"
    LOST_ARK = "lost_ark"

class GameNews(BaseModel):
    """게임 뉴스 통합 데이터 모델"""
    
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.isoformat()},
        use_enum_values=True
    )
    
    id: str = Field(..., description="뉴스 고유 ID")
    title: str = Field(..., description="뉴스 제목")
    content: Optional[str] = Field(None, description="뉴스 본문 내용")
    summary: Optional[str] = Field(None, description="뉴스 요약")
    url: HttpUrl = Field(..., description="뉴스 원본 URL")
    published_at: datetime = Field(..., description="발행 일시")
    game: GameType = Field(..., description="게임 타입")
    category: NewsType = Field(..., description="뉴스 카테고리")
    is_important: bool = Field(False, description="중요 공지 여부")
    tags: List[str] = Field(default_factory=list, description="태그 목록")
    view_count: Optional[int] = Field(None, description="조회수")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """제목 검증"""
        if not v or not v.strip():
            raise ValueError("제목은 필수입니다")
        return v.strip()
    
    @field_validator('published_at')
    @classmethod
    def validate_published_at(cls, v):
        """발행 일시 검증"""
        if v > datetime.now():
            raise ValueError("발행 일시는 현재 시간보다 미래일 수 없습니다")
        return v
    
    @field_validator('view_count')
    @classmethod
    def validate_view_count(cls, v):
        """조회수 검증"""
        if v is not None and v < 0:
            raise ValueError("조회수는 0 이상이어야 합니다")
        return v
    
    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return self.model_dump()
    
    def to_json(self) -> str:
        """JSON 문자열로 변환"""
        return self.model_dump_json()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GameNews':
        """딕셔너리에서 생성"""
        return cls(**data) 