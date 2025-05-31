from newsapi import NewsApiClient
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import News 
from core.config import settings
from dateutil import parser
import asyncio
from typing import List, Dict, Any

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

    async def load_news_to_db_concurrent(self, db: AsyncSession):
        semaphore = asyncio.Semaphore(3)
        
        async def fetch_category_news(category: str):
            async with semaphore:
                try:
                    loop = asyncio.get_event_loop()
                    data = await loop.run_in_executor(
                        None, 
                        lambda: self.newsapi.get_top_headlines(
                            language='en', page=1, page_size=50, category=category
                        )
                    )
                    articles = data.get('articles', [])
                    return self._filter_and_process_articles(articles, category)
                except Exception as e:
                    print(f"Error fetching {category} news: {e}")
                    return []
        
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

news_api_handler = NewsApiHandler()