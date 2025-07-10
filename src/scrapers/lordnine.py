"""로드나인 게임 스크래퍼"""

import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from src.scrapers.base import BaseScraper
from src.models.game_news import GameNews, GameType, NewsType
from src.models.exceptions import ScrapingException, ApiException
from src.utils.helpers import parse_timestamp, clean_text


class LordnineScraper(BaseScraper):
    """로드나인 게임 스크래퍼"""
    
    # API 설정
    BASE_URL = "https://api.onstove.com"
    
    # 게시판 ID
    BOARD_IDS = {
        "announcements": "128074",  # 공지사항
        "events": "128451",         # 이벤트
        "updates": "128074"         # 업데이트 (공지사항과 동일)
    }
    
    # 공통 API 파라미터
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
    
    def __init__(self, timeout: int = 30):
        """로드나인 스크래퍼 초기화"""
        super().__init__(GameType.LORDNINE, timeout)
        
    def get_default_headers(self) -> dict:
        """로드나인 API용 기본 헤더"""
        headers = super().get_default_headers()
        headers.update({
            'Accept': 'application/json',
            'Referer': 'https://page.onstove.com/',
            'Origin': 'https://page.onstove.com'
        })
        return headers
    
    async def get_announcements(self) -> List[GameNews]:
        """공지사항 목록 조회"""
        try:
            url = f"{self.BASE_URL}/cwms/v3.0/article_group/BOARD/{self.BOARD_IDS['announcements']}/article/list"
            response = await self.make_request(url, params=self.COMMON_PARAMS)
            data = response.json()
            
            if not self.validate_response_data(data, ['value']):
                raise ScrapingException("공지사항 응답 데이터 형식이 올바르지 않습니다")
            
            value_data = data.get('value', {})
            if 'list' not in value_data:
                raise ScrapingException("공지사항 응답에 'list' 키가 없습니다")
            
            articles = value_data.get('list', [])
            news_list = []
            
            for article in articles:
                try:
                    news = self._parse_article_data(article, NewsType.ANNOUNCEMENT)
                    if news:
                        news_list.append(news)
                except Exception as e:
                    # 개별 항목 파싱 실패는 로그만 남기고 계속 진행
                    continue
            
            return news_list
            
        except Exception as e:
            if isinstance(e, ScrapingException):
                raise
            raise ScrapingException(f"공지사항 조회 중 오류 발생: {str(e)}")
    
    async def get_announcement_detail(self, url: str) -> Optional[GameNews]:
        """공지사항 상세 조회"""
        return await self._get_detail(url, NewsType.ANNOUNCEMENT)
    
    async def get_events(self) -> List[GameNews]:
        """이벤트 목록 조회"""
        try:
            url = f"{self.BASE_URL}/cwms/v3.0/article_group/BOARD/{self.BOARD_IDS['events']}/article/list"
            response = await self.make_request(url, params=self.COMMON_PARAMS)
            data = response.json()
            
            if not self.validate_response_data(data, ['value']):
                raise ScrapingException("이벤트 응답 데이터 형식이 올바르지 않습니다")
            
            value_data = data.get('value', {})
            if 'list' not in value_data:
                raise ScrapingException("이벤트 응답에 'list' 키가 없습니다")
            
            articles = value_data.get('list', [])
            news_list = []
            
            for article in articles:
                try:
                    news = self._parse_article_data(article, NewsType.EVENT)
                    if news:
                        news_list.append(news)
                except Exception as e:
                    continue
            
            return news_list
            
        except Exception as e:
            if isinstance(e, ScrapingException):
                raise
            raise ScrapingException(f"이벤트 조회 중 오류 발생: {str(e)}")
    
    async def get_event_detail(self, url: str) -> Optional[GameNews]:
        """이벤트 상세 조회"""
        return await self._get_detail(url, NewsType.EVENT)
    
    async def get_updates(self) -> List[GameNews]:
        """업데이트 목록 조회"""
        try:
            # 업데이트는 공지사항에서 업데이트 관련 키워드로 필터링
            announcements = await self.get_announcements()
            
            # 업데이트 관련 키워드
            update_keywords = ['업데이트', '패치', '버전', '출시', '릴리스', '개선']
            
            updates = []
            for news in announcements:
                title_lower = news.title.lower()
                if any(keyword in title_lower for keyword in update_keywords):
                    # 카테고리를 업데이트로 변경
                    update_news = news.copy()
                    update_news.category = NewsType.UPDATE
                    updates.append(update_news)
            
            return updates
            
        except Exception as e:
            if isinstance(e, ScrapingException):
                raise
            raise ScrapingException(f"업데이트 조회 중 오류 발생: {str(e)}")
    
    async def get_update_detail(self, url: str) -> Optional[GameNews]:
        """업데이트 상세 조회"""
        return await self._get_detail(url, NewsType.UPDATE)
    
    async def _get_detail(self, url: str, category: NewsType) -> Optional[GameNews]:
        """상세 정보 조회 공통 메서드"""
        try:
            article_id = self._extract_article_id_from_url(url)
            if not article_id:
                raise ScrapingException(f"URL에서 article_id를 추출할 수 없습니다: {url}")
            
            # 상세 정보 API가 작동하지 않으므로, 목록에서 해당 항목을 찾아서 반환
            # 이는 임시 해결책이며, summary 정보를 content로 사용합니다
            
            # 카테고리에 따라 적절한 목록 조회
            if category == NewsType.ANNOUNCEMENT:
                articles_list = await self.get_announcements()
            elif category == NewsType.EVENT:
                articles_list = await self.get_events()
            elif category == NewsType.UPDATE:
                articles_list = await self.get_updates()
            else:
                articles_list = await self.get_announcements()
            
            # article_id가 일치하는 항목 찾기
            for article in articles_list:
                if article.id == article_id:
                    # summary를 content로 복사하여 상세 정보처럼 만들기
                    article.content = article.summary
                    return article
            
            # 찾지 못한 경우 None 반환
            return None
            
        except Exception as e:
            if isinstance(e, ScrapingException):
                raise
            raise ScrapingException(f"상세 정보 조회 중 오류 발생: {str(e)}")
    
    def _parse_article_data(self, article: Dict[str, Any], category: NewsType) -> Optional[GameNews]:
        """게시글 데이터를 GameNews로 변환"""
        try:
            # 필수 필드 확인
            if not all(key in article for key in ['article_id', 'title', 'create_datetime']):
                return None
            
            article_id = str(article['article_id'])
            title = article['title']
            create_datetime = article['create_datetime']
            
            # 타임스탬프 변환 (밀리초 단위)
            if isinstance(create_datetime, (int, float)):
                published_at = datetime.fromtimestamp(create_datetime / 1000)
            else:
                published_at = parse_timestamp(create_datetime)
            
            # URL 생성
            url = f"https://page.onstove.com/l9/global/view/{article_id}"
            
            # 중요도 판단
            is_important = self._is_important_article(article)
            
            # 태그 추출
            tags = self._extract_tags(article)
            
            # 조회수
            interaction_info = article.get('user_interaction_score_info', {})
            view_count = interaction_info.get('view_score', 0)
            
            # 요약
            summary = article.get('summary', '')
            
            return self.create_game_news(
                id=article_id,
                title=title,
                url=url,
                published_at=published_at,
                category=category,
                summary=summary,
                is_important=is_important,
                tags=tags,
                view_count=view_count
            )
            
        except Exception as e:
            return None
    
    def _parse_article_detail(self, article: Dict[str, Any], category: NewsType) -> Optional[GameNews]:
        """게시글 상세 데이터를 GameNews로 변환"""
        try:
            # 필수 필드 확인
            if not all(key in article for key in ['article_id', 'title', 'create_datetime']):
                return None
            
            article_id = str(article['article_id'])
            title = article['title']
            create_datetime = article['create_datetime']
            content = article.get('content', '')
            
            # 타임스탬프 변환 (밀리초 단위)
            if isinstance(create_datetime, (int, float)):
                published_at = datetime.fromtimestamp(create_datetime / 1000)
            else:
                published_at = parse_timestamp(create_datetime)
            
            # URL 생성
            url = f"https://page.onstove.com/l9/global/view/{article_id}"
            
            # 중요도 판단
            is_important = self._is_important_article(article)
            
            # 태그 추출
            tags = self._extract_tags(article)
            
            # 조회수
            interaction_info = article.get('user_interaction_score_info', {})
            view_count = interaction_info.get('view_score', 0)
            
            # 요약
            summary = article.get('summary', '')
            
            return self.create_game_news(
                id=article_id,
                title=title,
                content=content,
                url=url,
                published_at=published_at,
                category=category,
                summary=summary,
                is_important=is_important,
                tags=tags,
                view_count=view_count
            )
            
        except Exception as e:
            return None
    
    def _extract_article_id_from_url(self, url: str) -> Optional[str]:
        """URL에서 article_id 추출"""
        # https://page.onstove.com/l9/global/view/{article_id} 형식
        pattern = r'/view/(\d+)'
        match = re.search(pattern, url)
        return match.group(1) if match else None
    
    def _is_important_article(self, article: Dict[str, Any]) -> bool:
        """중요 게시글 판단"""
        title = article.get('title', '').lower()
        
        # headline_info에서 headline_name 추출
        headline_info = article.get('headline_info', {})
        headline_name = headline_info.get('headline_name', '').lower()
        
        # fixed_yn 확인 (Y/N 형태)
        is_fixed = article.get('fixed_yn', 'N') == 'Y'
        
        # admin_option_summary_info에서 공지 타입 확인
        admin_option = article.get('admin_option_summary_info', {})
        official_type = admin_option.get('official_type_code', '')
        notice_positions = admin_option.get('notice_position_code', [])
        
        # 고정 게시물이거나 중요 키워드가 포함된 경우
        important_keywords = ['공지', '점검', '긴급', '중요', '필독']
        
        return (is_fixed or 
                official_type in ['NOTICE', 'MAINTENANCE'] or
                'ALL' in notice_positions or
                any(keyword in title for keyword in important_keywords) or
                any(keyword in headline_name for keyword in important_keywords))
    
    def _extract_tags(self, article: Dict[str, Any]) -> List[str]:
        """게시글에서 태그 추출"""
        tags = []
        
        title = article.get('title', '').lower()
        
        # headline_info에서 headline_name 추출
        headline_info = article.get('headline_info', {})
        headline_name = headline_info.get('headline_name', '')
        
        # 말머리 태그 추가
        if headline_name:
            tags.append(headline_name)
        
        # admin_option_summary_info에서 공식 타입 추출
        admin_option = article.get('admin_option_summary_info', {})
        official_type = admin_option.get('official_type_code', '')
        if official_type:
            if official_type == 'NOTICE':
                tags.append('공지')
            elif official_type == 'MAINTENANCE':
                tags.append('점검')
        
        # 제목에서 태그 추출
        tag_keywords = {
            '공지': ['공지', '알림'],
            '이벤트': ['이벤트', '행사'],
            '점검': ['점검', '정기점검', '긴급점검'],
            '업데이트': ['업데이트', '패치', '버전'],
            '출시': ['출시', '릴리스', '런칭']
        }
        
        for tag, keywords in tag_keywords.items():
            if any(keyword in title for keyword in keywords):
                tags.append(tag)
        
        return list(set(tags))  # 중복 제거 