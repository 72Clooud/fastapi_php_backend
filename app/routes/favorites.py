from fastapi import APIRouter, Depends, HTTPException, status
from database.dependencis import get_db
from sqlalchemy.orm import Session
from schemas.post import PostInput
from schemas.favorites import FavoritePost
from auth.auth import auth
from models.post import Post
from models.favorites import Favorites
from typing import List

router = APIRouter(
    tags=['Favorites'],
    prefix='/favorite'
)


@router.post('/')
def favorites(post: PostInput, db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    post_exist = db.query(Post).filter(Post.url == str(post.url)).first()
    if not post_exist:
        new_post = Post(title=post.title, url=str(post.url))
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        post_id = new_post.id
    else:
        post_id = post_exist.id
    is_liked = db.query(Favorites).filter(
        Favorites.post_id == post_id,
        Favorites.user_id == current_user.id
    ).first()
    if not is_liked:
        new_favorite = Favorites(user_id=current_user.id, post_id=post_id)
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)
        return {"message": "Post added to favorites"}
    else:
        db.delete(is_liked)
        db.commit()
        return {"message": "Post removed from favorites"}
    
    
@router.get('/list', status_code=status.HTTP_200_OK, response_model=List[FavoritePost])
def get_favorites(db: Session = Depends(get_db), current_user: int = Depends(auth.get_current_user)):
    favorite_posts = db.query(Favorites).filter(Favorites.user_id == current_user.id).all()
    if not favorite_posts:
        return {"message": "Your favorites list is currently empty."}
    return [{"title": fav.post.title, "url": fav.post.url} for fav in favorite_posts]