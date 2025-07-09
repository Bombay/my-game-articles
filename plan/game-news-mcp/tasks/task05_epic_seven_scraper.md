# Task 05: 에픽세븐 게임 스크래퍼 구현

## 📋 체크리스트
- [ ] 에픽세븐 OnStove API 엔드포인트 구현
- [ ] 6가지 도구 메서드 구현
- [ ] board_seq를 이용한 카테고리별 데이터 수집
- [ ] 상세 정보 API 구현 (현재 미구현 상태)
- [ ] 제목 장식 및 중요도 판단 로직

## 📝 상세 내용
### 구현할 기능들
- OnStove API를 이용한 에픽세븐 뉴스 수집
- 카테고리별 board_seq 활용한 데이터 분류
- 조회수, 중요도에 따른 제목 이모지 장식
- 상세 정보 API 구현 (기존 문서에서 누락된 부분)

### API 엔드포인트 정보
```python
# 기본 설정
BASE_URL = "https://api.onstove.com/cwms/v3.0"
BOARD_SEQ = {
    "announcements": "995",
    "events": "1000",
    "updates": "997"
}

# 엔드포인트 패턴
LIST_ENDPOINT = "/article_group/BOARD/{board_seq}/article/list"
DETAIL_ENDPOINT = "/article/{article_id}"  # 구현 필요
```

## 🛠️ 기술적 세부사항
### 사용할 기술 스택
- **httpx**: 동기/비동기 HTTP 클라이언트
- **re**: article_id 추출 및 패턴 매칭
- **datetime**: UNIX 타임스탬프 변환

### 파일 구조
```
src/scrapers/
├── epic_seven.py      # 에픽세븐 스크래퍼 구현
└── base.py           # BaseScraper 추상 클래스
```

### 구현할 메서드
1. `get_announcements()` - 공지사항 리스트 (board_seq: 995)
2. `get_announcement_detail(url)` - 공지사항 상세 (구현 필요)
3. `get_events()` - 이벤트 리스트 (board_seq: 1000)
4. `get_event_detail(url)` - 이벤트 상세 (구현 필요)
5. `get_updates()` - 업데이트 리스트 (board_seq: 997)
6. `get_update_detail(url)` - 업데이트 상세 (구현 필요)

### 핵심 구현 요소
- 브라우저 유사 HTTP 헤더 (`User-Agent`, `Referer`, `x-client-lang`)
- UNIX 타임스탬프(밀리초) → datetime 변환
- 중요도(`📌`), 조회수(`🔥`), 카테고리(`📢`, `🎉`) 이모지 추가
- 페이지 사이즈 20개 고정

## ✅ 완료 조건
- [ ] 모든 6가지 도구가 정상 동작함
- [ ] 상세 정보 API가 새로 구현됨
- [ ] 제목 장식 로직이 적용됨
- [ ] 중요도 판단이 정확함
- [ ] 성능 요구사항 만족

### 검증 방법
```python
# 에픽세븐 스크래퍼 테스트
from src.scrapers.epic_seven import EpicSevenScraper

scraper = EpicSevenScraper()

# 공지사항 리스트 테스트
announcements = await scraper.get_announcements()
assert len(announcements) > 0
assert announcements[0].game == "epic_seven"

# 상세 정보 테스트 (새로 구현)
if announcements:
    detail = await scraper.get_announcement_detail(announcements[0].url)
    assert detail is not None
    assert detail.content is not None  # 이전엔 None 반환

# 이벤트 테스트
events = await scraper.get_events()
assert len(events) > 0
assert any("🎉" in event.title for event in events)  # 이벤트 이모지 확인

# 업데이트 테스트
updates = await scraper.get_updates()
assert len(updates) > 0
```