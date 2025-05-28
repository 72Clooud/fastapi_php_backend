from newsapi import NewsApiClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.news import News 
from schemas.news import NewsArticle
from core.config import settings
from datetime import datetime

class NewsApiHandler:
    def __init__(self):
        self.newsapi = NewsApiClient(api_key=settings.api_secret_key)
        self.categories = ['general', 'technology', 'business', 'science', 'sports', 'health', 'entertainment']
        
        
    async def load_news_to_db(self, db: AsyncSession):
            for category in self.categories:
                data = self.newsapi.get_top_headlines(language='en', page=1, page_size=50, category=category)
                article_raw = data['articles'] if 'articles' in data else []

                filtered_articles = [
                    a for a in article_raw
                    if a.get("description") and a.get("urlToImage")
                ]

                for a in filtered_articles:
                    result = await db.execute(select(News).where(News.url == str(a['url'])))
                    if result.scalar_one_or_none():
                        continue 
                    
                    news = News(
                        title=a.get("title"),
                        description=a.get("description"),
                        author=a.get("author"),
                        url=str(a.get("url")),
                        urlToImage=str(a.get("urlToImage")),
                        source_name=a.get("source", {}).get("name", ""),
                        category=category 
                    )
                    db.add(news)
            await db.commit()

news_api_handler = NewsApiHandler()