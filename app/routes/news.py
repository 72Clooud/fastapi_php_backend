from fastapi import APIRouter, Depends, HTTPException, status
from schemas.news import NewsArticleOut, NewsImageOut, Message
from services.news import news_api_handler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from database.database import db
from database.dependencis import get_db
from models.news import News
from typing import List, Union 


router = APIRouter(
    tags=['News'],
    prefix='/news'
)


@router.get('/', response_model=List[NewsArticleOut])
async def get_news(db: AsyncSession = Depends(get_db)):
    all_articles_result = await db.execute(select(News).order_by(desc(News.page)).limit(300))
    all_articles = all_articles_result.scalars().all()
    if not all_articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return all_articles


@router.get('/send/banner', response_model=List[NewsImageOut])
async def get_news_images(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(News.title, News.url, News.urlToImage).limit(30))
    rows = result.all()
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    
    return [NewsImageOut(title=title, url=url, urlToImage=urlToImage) for title, url, urlToImage in rows]


@router.get('/update', response_model=List[NewsArticleOut])
async def get_updated_news(db: AsyncSession = Depends(get_db)):
    await news_api_handler.load_news_to_db_concurrent(db)
    all_articles_result = await db.execute(select(News).order_by(desc(News.page)).limit(300))
    all_articles = all_articles_result.scalars().all()
    if not all_articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return all_articles


@router.get('/{category}', response_model=List[NewsArticleOut])
async def get_news_by_category(category: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(News).where(News.category == category).order_by(desc(News.page)))
    articles = result.scalars().all()
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")

    return articles