from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String)
    description = Column(String)
    url = Column(String, unique=True, nullable=False)
    urlToImage = Column(String, nullable=False)
    source_name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    
    favorited_by = relationship("Favorites", back_populates="post")