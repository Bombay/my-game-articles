# Task 06: 로스트아크 게임 스크래퍼 구현

## 📋 체크리스트
- [ ] Playwright를 이용한 동적 스크래핑 구현
- [ ] 6가지 도구 메서드 구현
- [ ] 브라우저 자동화 및 페이지 렌더링 처리
- [ ] 강건한 CSS 선택자 전략 구현
- [ ] 점검 공지 키워드 필터링 로직

## 📝 상세 내용
### 구현할 기능들
- Playwright를 이용한 JavaScript 렌더링 페이지 스크래핑
- 동적 콘텐츠 로드 대기 (`networkidle`)
- 여러 CSS 선택자를 순차 시도하는 강건한 추출 전략
- 점검 공지 키워드 필터링

### 대상 URL 정보
```python
BASE_URL = "https://lostark.game.onstove.com"
PATHS = {
    "announcements": "/News/Notice/List",
    "events": "/News/Event/Now", 
    "updates": "/News/Update/List"
}
```

## 🛠️ 기술적 세부사항
### 사용할 기술 스택
- **Playwright**: 브라우저 자동화 (Headless Chromium)
- **BeautifulSoup**: HTML 파싱 (선택적)
- **asyncio**: 비동기 처리

### 파일 구조
```
src/scrapers/
├── lost_ark.py       # 로스트아크 스크래퍼 구현
└── base.py          # BaseScraper 추상 클래스
```

### 구현할 메서드
1. `get_announcements()` - 공지사항 리스트
2. `get_announcement_detail(url)` - 공지사항 상세
3. `get_events()` - 이벤트 리스트
4. `get_event_detail(url)` - 이벤트 상세
5. `get_updates()` - 업데이트 리스트
6. `get_update_detail(url)` - 업데이트 상세

### 핵심 구현 요소
- **동적 스크래핑**: `wait_until='networkidle'`로 완전 로드 대기
- **강건한 선택자**: 다중 CSS 선택자 순차 시도
- **점검 필터링**: 제목에서 '점검', 'maintenance' 키워드 검색
- **카테고리 식별**: URL 경로로 뉴스 카테고리 판단

### 성능 최적화
- 브라우저 인스턴스 재사용
- 불필요한 리소스 로드 차단
- 타임아웃 설정

## ✅ 완료 조건
- [ ] Playwright가 정상 동작함
- [ ] 모든 6가지 도구가 구현됨
- [ ] 동적 콘텐츠가 올바르게 로드됨
- [ ] 강건한 선택자 전략이 동작함
- [ ] 점검 공지 필터링이 정확함

### 검증 방법
```python
# 로스트아크 스크래퍼 테스트
from src.scrapers.lost_ark import LostArkScraper

scraper = LostArkScraper()

# 공지사항 리스트 테스트
announcements = await scraper.get_announcements()
assert len(announcements) > 0
assert announcements[0].game == "lost_ark"

# 상세 정보 테스트
if announcements:
    detail = await scraper.get_announcement_detail(announcements[0].url)
    assert detail is not None
    assert detail.content is not None

# 이벤트 테스트
events = await scraper.get_events()
assert len(events) > 0

# 업데이트 테스트
updates = await scraper.get_updates()
assert len(updates) > 0

# 점검 공지 필터링 테스트 (선택적)
maintenance = await scraper.get_maintenance()
if maintenance:
    assert any("점검" in news.title.lower() for news in maintenance)

# 성능 테스트
import time
start = time.time()
await scraper.get_announcements()
duration = time.time() - start
assert duration < 10  # 10초 이내
```