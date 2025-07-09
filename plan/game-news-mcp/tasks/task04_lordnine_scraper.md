# Task 04: 로드나인 게임 스크래퍼 구현

## 📋 체크리스트
- [ ] 로드나인 API 엔드포인트 분석 및 구현
- [ ] 6가지 도구 메서드 구현
- [ ] API 요청 헤더 및 파라미터 설정
- [ ] 응답 데이터 파싱 및 GameNews 변환
- [ ] 에러 처리 및 재시도 로직

## 📝 상세 내용
### 구현할 기능들
- OnStove API를 이용한 로드나인 뉴스 수집
- 공지사항, 이벤트, 업데이트 각각의 리스트 및 상세 정보 수집
- API 응답 데이터의 GameNews 모델 변환
- 네트워크 오류 및 API 변경에 대한 대응

### API 엔드포인트 정보
```python
# 기본 설정
BASE_URL = "https://api.onstove.com"
BOARD_IDS = {
    "announcements": "128074",
    "events": "128451", 
    "updates": "128XXX"  # 문서에서 확인 필요
}

# 공통 파라미터
COMMON_PARAMS = {
    "interaction_type_code": "LIKE,DISLIKE,COMMENT,VIEW",
    "content_yn": "Y",
    "summary_yn": "Y",
    "sort_type_code": "LATEST",
    "headline_title_yn": "Y",
    "translation_yn": "N",
    "page": 1,
    "size": 24
}
```

## 🛠️ 기술적 세부사항
### 사용할 기술 스택
- **httpx**: 비동기 HTTP 클라이언트
- **re**: URL에서 article_id 추출
- **datetime**: 타임스탬프 변환

### 파일 구조
```
src/scrapers/
├── lordnine.py         # 로드나인 스크래퍼 구현
└── base.py            # BaseScraper 추상 클래스
```

### 구현할 메서드
1. `get_announcements()` - 공지사항 리스트
2. `get_announcement_detail(url)` - 공지사항 상세
3. `get_events()` - 이벤트 리스트
4. `get_event_detail(url)` - 이벤트 상세
5. `get_updates()` - 업데이트 리스트
6. `get_update_detail(url)` - 업데이트 상세

### 핵심 로직
- API 호출 시 적절한 User-Agent 설정
- UNIX 타임스탬프 → datetime 변환
- 제목 키워드 분석으로 중요도 판단
- URL에서 article_id 추출하여 상세 정보 조회

## ✅ 완료 조건
- [ ] 모든 6가지 도구가 정상 동작함
- [ ] API 응답이 올바르게 GameNews로 변환됨
- [ ] 네트워크 오류 처리가 구현됨
- [ ] 상세 정보 조회가 정상 동작함
- [ ] 성능 요구사항 만족 (리스트 10초, 상세 15초 이내)

### 검증 방법
```python
# 로드나인 스크래퍼 테스트
from src.scrapers.lordnine import LordnineScraper

scraper = LordnineScraper()

# 공지사항 리스트 테스트
announcements = await scraper.get_announcements()
assert len(announcements) > 0
assert all(isinstance(news, GameNews) for news in announcements)

# 상세 정보 테스트
if announcements:
    detail = await scraper.get_announcement_detail(announcements[0].url)
    assert detail is not None
    assert detail.content is not None

# 이벤트 및 업데이트 테스트
events = await scraper.get_events()
updates = await scraper.get_updates()
assert len(events) > 0
assert len(updates) > 0
```