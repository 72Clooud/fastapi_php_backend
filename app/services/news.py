from newsapi import NewsApiClient
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News 
from core.config import settings
from dateutil import parser
import asyncio
from typing import List, Dict, Any, Set
from sqlalchemy import select

class NewsApiHandler:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=settings.api_secret_key)
        self.categories = ['general', 'technology', 'business', 'science', 'sports', 'health', 'entertainment']
    
    def _filter_and_process_articles(self, articles: List[Dict[Any, Any]], category: str) -> List[Dict[str, Any]]:
        processed = []
        for a in articles:
            if not (a.get("description") and a.get("urlToImage") and a.get("url")):
                continue
                
            try:
                processed_article = {
                    'title': a.get("title"),
                    'description': a.get("description"),
                    'author': a.get("author"),
                    'url': str(a.get("url")),
                    'publishedAt': parser.isoparse(a.get("publishedAt")),
                    'urlToImage': str(a.get("urlToImage")),
                    'source_name': a.get("source", {}).get("name", ""),
                    'category': category
                }
                processed.append(processed_article)
            except (ValueError, TypeError):
                continue

        return processed
    
    async def _get_existing_urls(self, db: AsyncSession, urls: List[str]) -> Set[str]:
        if not urls:
            return set()
            
        result = await db.execute(
            select(News.url).where(News.url.in_(urls))
        )
        return {row[0] for row in result.fetchall()}

    async def _fetch_articles_from_api(self, category: str, page_size: int = 100, page: int = 1) -> List[Dict[str, Any]]:
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None, 
                lambda: self.newsapi.get_top_headlines(
                    language='en', page=page, page_size=page_size, category=category
                )
            )
            articles = data.get('articles', [])
            return self._filter_and_process_articles(articles, category)
        except Exception as e:
            print(f"Error fetching {category} news: {e}")
            return []

    async def load_news_to_db_concurrent(self, db: AsyncSession):
        semaphore = asyncio.Semaphore(3)
        
        async def fetch_category_news(category: str):
            async with semaphore:
                return await self._fetch_articles_from_api(category, page_size=50)
        
        tasks = [fetch_category_news(cat) for cat in self.categories]
        results = await asyncio.gather(*tasks)
        
        all_articles = []
        seen_urls = set()
        
        for articles in results:
            for article in articles:
                url = article['url']
                if url not in seen_urls:
                    seen_urls.add(url)
                    all_articles.append(article)
        
        if not all_articles:
            return
        
        all_urls = [a['url'] for a in all_articles]
        existing_urls = await self._get_existing_urls(db, all_urls)
        
        new_articles = []
        for article_data in all_articles:
            if article_data['url'] not in existing_urls:
                try:
                    news = News(**article_data)
                    new_articles.append(news)
                except Exception as e:
                    print(f"Error creating News object: {e}")
                    continue
        
        if new_articles:
            try:
                db.add_all(new_articles)
                await db.commit()
                print(f"Added {len(new_articles)} new articles to database")
            except Exception as e:
                print(f"Error inserting articles: {e}")
                await db.rollback()
        else:
            print("No new articles to add")

    async def load_random_unique_news_to_db(self, db: AsyncSession, count: int = 20):
        unique_new_articles: List[News] = []
        fetched_urls: Set[str] = set()
        pages_to_check = 5
        articles_per_page = 100
        
        for category in self.categories:
            if len(unique_new_articles) >= count:
                break
            for page in range(1, pages_to_check + 1):
                if len(unique_new_articles) >= count:
                    break
                
                articles = await self._fetch_articles_from_api(category, page_size=articles_per_page, page=page)
                
                current_batch_urls = [a['url'] for a in articles]
                
                existing_urls = await self._get_existing_urls(db, current_batch_urls)
                
                for article_data in articles:
                    url = article_data['url']
                    if url not in existing_urls and url not in fetched_urls:
                        try:
                            news = News(**article_data)
                            unique_new_articles.append(news)
                            fetched_urls.add(url)
                            if len(unique_new_articles) >= count:
                                break
                        except Exception as e:
                            print(f"Error creating News object for URL {url}: {e}")
                            continue

        if unique_new_articles:
            try:
                db.add_all(unique_new_articles)
                await db.commit()
                print(f"Added {len(unique_new_articles)} random unique articles to database")
            except Exception as e:
                print(f"Error inserting random unique articles: {e}")
                await db.rollback()
        else:
            print("No new random unique articles to add.")


news_api_handler = NewsApiHandler()