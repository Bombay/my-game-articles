# Task 03: 공통 데이터 모델 및 유틸리티 구현

## 📋 체크리스트
- [ ] GameNews 데이터 모델 생성
- [ ] BaseScraper 추상 클래스 구현
- [ ] 공통 유틸리티 함수 작성
- [ ] 데이터 검증 및 직렬화 로직
- [ ] 에러 처리 및 예외 클래스 정의

## 📝 상세 내용
### 구현할 기능들
- 모든 게임 뉴스를 위한 통합 데이터 모델
- 스크래퍼 구현을 위한 기본 클래스
- 날짜 처리, URL 검증 등 공통 유틸리티
- 일관된 응답 형식 보장

### 코드 예시
```python
# src/models/game_news.py
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List
from enum import Enum

class NewsType(str, Enum):
    ANNOUNCEMENT = "announcement"
    EVENT = "event"
    UPDATE = "update"

class GameNews(BaseModel):
    id: str
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    url: HttpUrl
    published_at: datetime
    game: str
    category: NewsType
    is_important: bool = False
    tags: List[str] = []
    view_count: Optional[int] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

## 🛠️ 기술적 세부사항
### 사용할 기술 스택
- **Pydantic**: 데이터 검증 및 직렬화
- **ABC**: 추상 클래스 구현
- **datetime**: 날짜 처리
- **re**: 정규표현식 (URL 파싱)

### 파일 구조
```
src/
├── models/
│   ├── __init__.py
│   ├── game_news.py    # 게임 뉴스 데이터 모델
│   └── exceptions.py   # 커스텀 예외 클래스
├── scrapers/
│   ├── __init__.py
│   └── base.py         # BaseScraper 추상 클래스
└── utils/
    ├── __init__.py
    ├── helpers.py      # 공통 유틸리티 함수
    └── validators.py   # 데이터 검증 함수
```

### 핵심 구현 요소
1. **GameNews 모델**: 모든 게임 뉴스의 통합 데이터 구조
2. **BaseScraper**: 각 게임 스크래퍼의 공통 인터페이스
3. **공통 유틸리티**: 날짜 파싱, URL 검증, 텍스트 정제
4. **예외 처리**: 스크래핑 실패, 네트워크 오류 등

## ✅ 완료 조건
- [ ] GameNews 모델이 올바르게 정의됨
- [ ] BaseScraper 추상 클래스가 구현됨
- [ ] 공통 유틸리티 함수들이 작성됨
- [ ] 데이터 검증이 정상 동작함
- [ ] 예외 클래스들이 정의됨

### 검증 방법
```python
# 데이터 모델 테스트
from src.models.game_news import GameNews, NewsType

news = GameNews(
    id="test-1",
    title="테스트 뉴스",
    url="https://example.com/news/1",
    published_at=datetime.now(),
    game="lordnine",
    category=NewsType.ANNOUNCEMENT
)

# 직렬화 테스트
json_data = news.model_dump_json()
print(json_data)

# 스크래퍼 인터페이스 테스트
from src.scrapers.base import BaseScraper
# 각 게임 스크래퍼가 올바른 인터페이스를 구현하는지 확인
```