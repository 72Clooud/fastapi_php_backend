from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.user import User

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False, unique=True)

    liked_by = relationship("User", secondary="favorites", back_populates="favorites_posts")