from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
   
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User
    from models.post import Post

class Favorites(Base):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)
    
