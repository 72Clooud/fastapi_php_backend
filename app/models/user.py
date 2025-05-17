from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Date
from sqlalchemy.orm import relationship
from database.database import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.post import Post

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False, unique=True)
    dateOfBirth = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))

    favorites_posts = relationship("Post", secondary="favorites", back_populates="liked_by")