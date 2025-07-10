"""로스트아크 게임 스크래퍼"""

import re
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime
from playwright.async_api import async_playwright, Browser, Page

from src.scrapers.base import BaseScraper
from src.models.game_news import GameNews, GameType, NewsType
from src.models.exceptions import ScrapingException, TimeoutException
from src.utils.helpers import parse_timestamp, clean_text


class LostArkScraper(BaseScraper):
    """로스트아크 게임 스크래퍼"""
    
    # 기본 설정
    BASE_URL = "https://lostark.game.onstove.com"
    
    # 페이지 경로
    PATHS = {
        "announcements": "/News/Notice/List",
        "events": "/News/Event/Now", 
        "updates": "/News/Update/List"
    }
    
    def __init__(self, timeout: int = 30):
        """로스트아크 스크래퍼 초기화"""
        super().__init__(GameType.LOST_ARK, timeout)
        self.browser: Optional[Browser] = None
        self.playwright = None
        
    async def init_browser(self):
        """브라우저 초기화"""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
    
    async def close_browser(self):
        """브라우저 종료"""
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        await self.init_browser()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        await self.close_browser()
    
    async def create_page(self) -> Page:
        """새 페이지 생성"""
        if not self.browser:
            await self.init_browser()
        
        assert self.browser is not None
        page = await self.browser.new_page()
        
        # 브라우저 설정
        await page.set_viewport_size({"width": 1920, "height": 1080})
        await page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        return page
    
    async def get_announcements(self) -> List[GameNews]:
        """공지사항 목록 조회"""
        return await self._get_news_list(NewsType.ANNOUNCEMENT, "announcements")
    
    async def get_announcement_detail(self, url: str) -> Optional[GameNews]:
        """공지사항 상세 조회"""
        return await self._get_news_detail(url, NewsType.ANNOUNCEMENT)
    
    async def get_events(self) -> List[GameNews]:
        """이벤트 목록 조회"""
        return await self._get_news_list(NewsType.EVENT, "events")
    
    async def get_event_detail(self, url: str) -> Optional[GameNews]:
        """이벤트 상세 조회"""
        return await self._get_news_detail(url, NewsType.EVENT)
    
    async def get_updates(self) -> List[GameNews]:
        """업데이트 목록 조회"""
        return await self._get_news_list(NewsType.UPDATE, "updates")
    
    async def get_update_detail(self, url: str) -> Optional[GameNews]:
        """업데이트 상세 조회"""
        return await self._get_news_detail(url, NewsType.UPDATE)
    
    async def _get_news_list(self, category: NewsType, path_key: str) -> List[GameNews]:
        """뉴스 목록 조회 공통 메서드"""
        try:
            page = await self.create_page()
            
            try:
                url = f"{self.BASE_URL}{self.PATHS[path_key]}"
                await page.goto(url, wait_until='networkidle', timeout=self.timeout * 1000)
                
                # 페이지 로드 대기
                await page.wait_for_timeout(2000)
                
                # 뉴스 목록 추출
                news_list = await self._extract_news_list(page, category)
                
                return news_list
                
            finally:
                await page.close()
                
        except Exception as e:
            if "timeout" in str(e).lower():
                raise TimeoutException(f"{category.value} 목록 조회 타임아웃", self.timeout)
            raise ScrapingException(f"{category.value} 목록 조회 중 오류 발생: {str(e)}")
    
    async def _extract_news_list(self, page: Page, category: NewsType) -> List[GameNews]:
        """페이지에서 뉴스 목록 추출"""
        news_list = []
        
        try:
            # 로스트아크 실제 구조에 맞는 선택자
            selectors = [
                'a[href*="Notice/View"]',  # 공지사항
                'a[href*="Event/View"]',   # 이벤트  
                'a[href*="Update/View"]',  # 업데이트
                'a[href*="/View/"]',       # 일반 View 링크
                'table tr',               # 테이블 행
                '.board tbody tr'         # 게시판 테이블 행
            ]
            
            articles = None
            for selector in selectors:
                try:
                    articles = await page.query_selector_all(selector)
                    if articles and len(articles) > 5:  # 최소 5개 이상 찾은 경우만
                        break
                except:
                    continue
            
            # 카테고리별 특정 링크 패턴 사용
            if category == NewsType.ANNOUNCEMENT:
                articles = await page.query_selector_all('a[href*="Notice/View"]')
            elif category == NewsType.EVENT:
                # 이벤트는 다양한 패턴 시도
                event_articles = await page.query_selector_all('a[href*="Event/View"]')
                if not event_articles:
                    event_articles = await page.query_selector_all('a[href*="/Event/"]')
                articles = event_articles
            elif category == NewsType.UPDATE:
                # 업데이트도 다양한 패턴 시도
                update_articles = await page.query_selector_all('a[href*="Update/View"]')
                if not update_articles:
                    update_articles = await page.query_selector_all('a[href*="/Update/"]')
                articles = update_articles
            
            if not articles:
                return news_list
            
            for article in articles[:20]:  # 최대 20개
                try:
                    news = await self._parse_article_element(article, category, page)
                    if news:
                        news_list.append(news)
                except Exception as e:
                    # 개별 항목 파싱 실패는 무시하고 계속 진행
                    continue
                    
        except Exception as e:
            raise ScrapingException(f"뉴스 목록 추출 중 오류: {str(e)}")
        
        return news_list
    
    async def _parse_article_element(self, element, category: NewsType, page: Page) -> Optional[GameNews]:
        """개별 기사 요소 파싱"""
        try:
            # 제목 추출 (여러 선택자 시도)
            title_selectors = [
                '.title', '.subject', '.tit', 'h3', 'h4', 
                '.news-title', '.notice-title', 'strong'
            ]
            
            title = None
            for selector in title_selectors:
                try:
                    title_element = await element.query_selector(selector)
                    if title_element:
                        title = await title_element.inner_text()
                        title = clean_text(title)
                        break
                except:
                    continue
            
            # 제목이 없으면 전체 텍스트에서 추출
            if not title:
                title = await element.inner_text()
                title = clean_text(title.split('\n')[0])
            
            if not title:
                return None
            
            # URL 추출 (element가 이미 링크인 경우)
            url = None
            try:
                # element 자체가 a 태그인 경우
                href = await element.get_attribute('href')
                if href:
                    if href.startswith('/'):
                        url = f"{self.BASE_URL}{href}"
                    elif href.startswith('http'):
                        url = href
                    else:
                        # 상대 경로인 경우
                        url = f"{self.BASE_URL}/{href.lstrip('/')}"
            except:
                pass
            
            if not url:
                return None
            
            # 날짜 추출
            date_selectors = [
                '.date', '.time', '.regdate', '.created', 
                '.publish-date', '.write-date'
            ]
            
            published_at = datetime.now()
            for selector in date_selectors:
                try:
                    date_element = await element.query_selector(selector)
                    if date_element:
                        date_text = await date_element.inner_text()
                        published_at = parse_timestamp(date_text)
                        break
                except:
                    continue
            
            # ID 생성 (URL에서 추출)
            article_id = self._extract_id_from_url(url)
            if not article_id:
                article_id = str(hash(url))[-8:]  # URL 해시 사용
            
            # 중요도 판단
            is_important = self._is_important_news(title)
            
            # 점검 공지 필터링
            if self._is_maintenance_notice(title):
                # 점검 공지는 태그를 추가하되 포함시킴
                tags = ['점검', 'maintenance']
            else:
                tags = self._extract_tags_from_title(title)
            
            return self.create_game_news(
                id=article_id,
                title=title,
                url=url,
                published_at=published_at,
                category=category,
                is_important=is_important,
                tags=tags
            )
            
        except Exception as e:
            return None
    
    async def _get_news_detail(self, url: str, category: NewsType) -> Optional[GameNews]:
        """뉴스 상세 정보 조회"""
        try:
            page = await self.create_page()
            
            try:
                await page.goto(str(url), wait_until='networkidle', timeout=self.timeout * 1000)
                await page.wait_for_timeout(2000)
                
                # 상세 내용 추출
                content = await self._extract_detail_content(page)
                
                # 기본 정보는 목록에서 가져온 것을 사용
                article_id = self._extract_id_from_url(str(url))
                if not article_id:
                    article_id = str(hash(url))[-8:]
                
                # 제목 추출
                title_selectors = [
                    '.view-title', '.detail-title', '.content-title',
                    'h1', 'h2', '.title', '.subject'
                ]
                
                title = None
                for selector in title_selectors:
                    try:
                        title_element = await page.query_selector(selector)
                        if title_element:
                            title = await title_element.inner_text()
                            title = clean_text(title)
                            break
                    except:
                        continue
                
                if not title:
                    title = "제목 없음"
                
                # 날짜 추출
                date_selectors = [
                    '.view-date', '.detail-date', '.publish-date',
                    '.date', '.time', '.regdate'
                ]
                
                published_at = datetime.now()
                for selector in date_selectors:
                    try:
                        date_element = await page.query_selector(selector)
                        if date_element:
                            date_text = await date_element.inner_text()
                            published_at = parse_timestamp(date_text)
                            break
                    except:
                        continue
                
                # 중요도 및 태그
                is_important = self._is_important_news(title)
                tags = self._extract_tags_from_title(title)
                
                if self._is_maintenance_notice(title):
                    tags.extend(['점검', 'maintenance'])
                
                return self.create_game_news(
                    id=article_id,
                    title=title,
                    url=str(url),
                    published_at=published_at,
                    category=category,
                    content=content,
                    summary=content[:200] + "..." if content and len(content) > 200 else content,
                    is_important=is_important,
                    tags=list(set(tags))  # 중복 제거
                )
                
            finally:
                await page.close()
                
        except Exception as e:
            if "timeout" in str(e).lower():
                raise TimeoutException(f"상세 정보 조회 타임아웃: {url}", self.timeout)
            raise ScrapingException(f"상세 정보 조회 중 오류 발생: {str(e)}")
    
    async def _extract_detail_content(self, page: Page) -> Optional[str]:
        """상세 페이지에서 본문 내용 추출"""
        content_selectors = [
            '.view-content', '.detail-content', '.content-body',
            '.article-content', '.news-content', '.notice-content',
            '.content', '.body', '.text'
        ]
        
        for selector in content_selectors:
            try:
                content_element = await page.query_selector(selector)
                if content_element:
                    content = await content_element.inner_text()
                    return clean_text(content)
            except:
                continue
        
        return None
    
    def _extract_id_from_url(self, url: str) -> Optional[str]:
        """URL에서 ID 추출"""
        if not isinstance(url, str):
            return None
        
        patterns = [
            r'/view/(\d+)',
            r'/detail/(\d+)', 
            r'id=(\d+)',
            r'no=(\d+)',
            r'/(\d+)$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _is_important_news(self, title: str) -> bool:
        """뉴스 중요도 판단"""
        if not title:
            return False
        
        title_lower = title.lower()
        
        important_keywords = [
            '긴급', '중요', '공지', '안내', '업데이트', '패치',
            '점검', '오픈', '출시', '종료', '마감', '이벤트'
        ]
        
        return any(keyword in title_lower for keyword in important_keywords)
    
    def _is_maintenance_notice(self, title: str) -> bool:
        """점검 공지 여부 판단"""
        if not title:
            return False
        
        title_lower = title.lower()
        maintenance_keywords = [
            '점검', 'maintenance', '서버점검', '정기점검', 
            '긴급점검', '임시점검', '시스템점검'
        ]
        
        return any(keyword in title_lower for keyword in maintenance_keywords)
    
    def _extract_tags_from_title(self, title: str) -> List[str]:
        """제목에서 태그 추출"""
        if not title:
            return []
        
        tags = []
        
        # 대괄호 안의 내용 추출
        bracket_matches = re.findall(r'\[([^\]]+)\]', title)
        tags.extend(bracket_matches)
        
        # 키워드 기반 태그
        keyword_tags = {
            '업데이트': ['업데이트', 'update'],
            '패치': ['패치', 'patch'],
            '이벤트': ['이벤트', 'event'],
            '점검': ['점검', 'maintenance'],
            '공지': ['공지', 'notice'],
            '출시': ['출시', 'release'],
            '종료': ['종료', 'end']
        }
        
        title_lower = title.lower()
        for keyword, tag_list in keyword_tags.items():
            if keyword in title_lower:
                tags.extend(tag_list)
        
        return list(set(tags))  # 중복 제거 