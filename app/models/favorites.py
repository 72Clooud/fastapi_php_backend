from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
   
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.news import News

class Favorites(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("news.id"), primary_key=True)
    
    user = relationship("User", back_populates="favorites")
    post = relationship("News", back_populates="favorited_by")