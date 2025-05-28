from fastapi import APIRouter, Depends, HTTPException, status
from database.dependencis import get_db
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas.post import PostInput
from schemas.favorites import FavoritePost
from auth.auth import auth
from models.news import News
from models.favorites import Favorites
from typing import List

router = APIRouter(
    tags=['Favorites'],
    prefix='/favorite'
)


@router.post('/')
async def favorites(post: PostInput, db: AsyncSession = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    post_result = await db.execute(select(News).filter(News.id == post.id))
    post_exist = post_result.scalar_one_or_none()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post with this url is not exits")
    like_result = await db.execute(select(Favorites).where(
        Favorites.post_id == post.id,
        Favorites.user_id == current_user.id
    ))
    is_liked = like_result.scalar_one_or_none()
    if not is_liked:
        new_favorite = Favorites(user_id=current_user.id, post_id=post.id)
        db.add(new_favorite)
        await db.commit()
        await db.refresh(new_favorite)
        return {"message": "Post added to favorites"}
    else:
        await db.delete(is_liked)
        await db.commit()
        return {"message": "Post removed from favorites"}
    
    
@router.get('/list', status_code=status.HTTP_200_OK, response_model=List[FavoritePost])
async def get_favorites(db: AsyncSession = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    favorite_posts_result = await db.execute(
        select(Favorites)
        .options(selectinload(Favorites.post))
        .where(Favorites.user_id == current_user.id)
    )
    favorite_posts = favorite_posts_result.scalars().all()
    if not favorite_posts:
        return {"message": "Your favorites list is currently empty."}
    return [{"title": fav.post.title, "url": fav.post.url, 'urlToImage': fav.post.urlToImage} for fav in favorite_posts]