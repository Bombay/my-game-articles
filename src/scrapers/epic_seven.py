"""에픽세븐 게임 스크래퍼"""

import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from src.scrapers.base import BaseScraper
from src.models.game_news import GameNews, GameType, NewsType
from src.models.exceptions import ScrapingException, ApiException
from src.utils.helpers import parse_timestamp, clean_text


class EpicSevenScraper(BaseScraper):
    """에픽세븐 게임 스크래퍼"""
    
    # API 설정
    BASE_URL = "https://api.onstove.com/cwms/v3.0"
    
    # 게시판 ID (board_seq)
    BOARD_SEQ = {
        "announcements": "995",   # 공지사항
        "events": "1000",         # 이벤트
        "updates": "997"          # 업데이트
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
        "size": 20  # 에픽세븐은 20개 고정
    }
    
    def __init__(self, timeout: int = 30):
        """에픽세븐 스크래퍼 초기화"""
        super().__init__(GameType.EPIC_SEVEN, timeout)
        
    def get_default_headers(self) -> dict:
        """에픽세븐 API용 기본 헤더"""
        headers = super().get_default_headers()
        headers.update({
            'Accept': 'application/json',
            'Referer': 'https://page.onstove.com/epicseven/global',
            'Origin': 'https://page.onstove.com',
            'x-client-lang': 'ko'
        })
        return headers
    
    async def get_announcements(self) -> List[GameNews]:
        """공지사항 목록 조회"""
        try:
            url = f"{self.BASE_URL}/article_group/BOARD/{self.BOARD_SEQ['announcements']}/article/list"
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
            url = f"{self.BASE_URL}/article_group/BOARD/{self.BOARD_SEQ['events']}/article/list"
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
            url = f"{self.BASE_URL}/article_group/BOARD/{self.BOARD_SEQ['updates']}/article/list"
            response = await self.make_request(url, params=self.COMMON_PARAMS)
            data = response.json()
            
            if not self.validate_response_data(data, ['value']):
                raise ScrapingException("업데이트 응답 데이터 형식이 올바르지 않습니다")
            
            value_data = data.get('value', {})
            if 'list' not in value_data:
                raise ScrapingException("업데이트 응답에 'list' 키가 없습니다")
            
            articles = value_data.get('list', [])
            news_list = []
            
            for article in articles:
                try:
                    news = self._parse_article_data(article, NewsType.UPDATE)
                    if news:
                        news_list.append(news)
                except Exception as e:
                    continue
            
            return news_list
            
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
            
            # 상세 정보 API 구현
            detail_url = f"{self.BASE_URL}/article/{article_id}"
            params = {
                "interaction_type_code": "LIKE,DISLIKE,COMMENT,VIEW",
                "content_yn": "Y"
            }
            
            try:
                response = await self.make_request(detail_url, params=params)
                data = response.json()
                
                if not self.validate_response_data(data, ['value']):
                    raise ScrapingException("상세 정보 응답 데이터 형식이 올바르지 않습니다")
                
                article = data.get('value', {})
                return self._parse_article_detail(article, category)
                
            except Exception as e:
                # 상세 API 실패 시 목록에서 찾기 (fallback)
                return await self._get_detail_from_list(article_id, category)
            
        except Exception as e:
            if isinstance(e, ScrapingException):
                raise
            raise ScrapingException(f"상세 정보 조회 중 오류 발생: {str(e)}")
    
    async def _get_detail_from_list(self, article_id: str, category: NewsType) -> Optional[GameNews]:
        """목록에서 상세 정보 찾기 (fallback)"""
        try:
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
            
            return None
            
        except Exception as e:
            raise ScrapingException(f"목록에서 상세 정보 찾기 실패: {str(e)}")
    
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
            url = f"https://page.onstove.com/epicseven/global/view/{article_id}"
            
            # 내용 및 요약
            content = article.get('content', '')
            summary = article.get('summary', '')
            
            # 조회수
            view_count = article.get('view_count', 0)
            
            # 중요도 판단
            is_important = self._is_important_article(article)
            
            # 태그 추출
            tags = self._extract_tags(article)
            
            # 제목 장식
            decorated_title = self._decorate_title(title, category, is_important, view_count)
            
            return self.create_game_news(
                id=article_id,
                title=decorated_title,
                url=url,
                published_at=published_at,
                category=category,
                content=content,
                summary=summary,
                is_important=is_important,
                tags=tags,
                view_count=view_count
            )
            
        except Exception as e:
            return None
    
    def _parse_article_detail(self, article: Dict[str, Any], category: NewsType) -> Optional[GameNews]:
        """상세 게시글 데이터를 GameNews로 변환"""
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
            url = f"https://page.onstove.com/epicseven/global/view/{article_id}"
            
            # 내용 및 요약 (상세 정보에서는 content가 더 상세함)
            content = article.get('content', '')
            summary = article.get('summary', '')
            
            # 조회수
            view_count = article.get('view_count', 0)
            
            # 중요도 판단
            is_important = self._is_important_article(article)
            
            # 태그 추출
            tags = self._extract_tags(article)
            
            # 제목 장식
            decorated_title = self._decorate_title(title, category, is_important, view_count)
            
            return self.create_game_news(
                id=article_id,
                title=decorated_title,
                url=url,
                published_at=published_at,
                category=category,
                content=content,
                summary=summary,
                is_important=is_important,
                tags=tags,
                view_count=view_count
            )
            
        except Exception as e:
            return None
    
    def _extract_article_id_from_url(self, url: str) -> Optional[str]:
        """URL에서 article_id 추출"""
        if not isinstance(url, str):
            return None
        
        # 에픽세븐 URL 패턴: https://page.onstove.com/epicseven/global/view/10867009
        match = re.search(r'/view/(\d+)', url)
        if match:
            return match.group(1)
        
        # 다른 패턴들도 시도
        patterns = [
            r'article_id=(\d+)',      # article_id=12345
            r'/(\d+)$',               # 끝에 있는 숫자
            r'/(\d+)/',               # 중간에 있는 숫자
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _is_important_article(self, article: Dict[str, Any]) -> bool:
        """게시글 중요도 판단"""
        title = article.get('title', '').lower()
        
        # 중요 키워드
        important_keywords = [
            '긴급', '중요', '점검', '공지', '안내', '업데이트', '패치',
            '이벤트', '출시', '릴리스', '오픈', '종료', '마감'
        ]
        
        # 제목에 중요 키워드가 포함되어 있는지 확인
        if any(keyword in title for keyword in important_keywords):
            return True
        
        # 고정 게시물 여부 확인
        if article.get('is_headline', False) or article.get('is_top', False):
            return True
        
        # 조회수가 높은 경우
        view_count = article.get('view_count', 0)
        if view_count > 10000:
            return True
        
        return False
    
    def _extract_tags(self, article: Dict[str, Any]) -> List[str]:
        """게시글에서 태그 추출"""
        tags = []
        
        title = article.get('title', '')
        
        # 말머리 추출 (대괄호 안의 내용)
        bracket_matches = re.findall(r'\[([^\]]+)\]', title)
        tags.extend(bracket_matches)
        
        # 카테고리 정보
        category = article.get('category', '')
        if category:
            tags.append(category)
        
        # 공식 타입
        article_type = article.get('article_type', '')
        if article_type:
            tags.append(article_type)
        
        # 제목에서 키워드 추출
        title_keywords = ['점검', '업데이트', '패치', '이벤트', '출시', '종료']
        for keyword in title_keywords:
            if keyword in title:
                tags.append(keyword)
        
        return list(set(tags))  # 중복 제거
    
    def _decorate_title(self, title: str, category: NewsType, is_important: bool, view_count: int) -> str:
        """제목 장식 (이모지 추가)"""
        decorated_title = title
        
        # 중요도 이모지
        if is_important:
            decorated_title = f"📌 {decorated_title}"
        
        # 조회수 이모지 (10,000 이상)
        if view_count >= 10000:
            decorated_title = f"🔥 {decorated_title}"
        
        # 카테고리별 이모지
        if category == NewsType.ANNOUNCEMENT:
            decorated_title = f"📢 {decorated_title}"
        elif category == NewsType.EVENT:
            decorated_title = f"🎉 {decorated_title}"
        elif category == NewsType.UPDATE:
            decorated_title = f"🔄 {decorated_title}"
        
        return decorated_title 