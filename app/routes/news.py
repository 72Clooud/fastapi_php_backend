from fastapi import APIRouter, Depends, HTTPException, status
from schemas.news import NewsArticleOut, NewsImageOut
from services.news import news_api_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.dependencis import get_db
from models.news import News
from typing import List 


router = APIRouter(
    tags=['News']
)


@router.get('/news', response_model=List[NewsArticleOut])
async def get_news(db: AsyncSession = Depends(get_db)):
    all_articles_result = await db.execute(select(News))
    all_articles = all_articles_result.scalars().all()
    if not all_articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return all_articles


@router.get('/news/{category}', response_model=List[NewsArticleOut])
async def get_news_by_category(category: str, db: AsyncSession = Depends(get_db)):
    query = select(News).where(News.category == category)
    result = await db.execute(query)
    articles = result.scalars().all()

    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return articles


@router.get('/news/send/images', response_model=List[NewsImageOut])
async def get_news_images(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(News.urlToImage).limit(30))
    urls = result.scalars().all()
    return [NewsImageOut(urlToImage=url) for url in urls]