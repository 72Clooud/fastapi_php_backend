from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    message: str
    class Config:
        from_attributes = True

class NewsArticle(BaseModel):
    title: str
    description: Optional[str]
    publishedAt: datetime
    url: str
    urlToImage: Optional[str]
    source: dict
    category: str
    
class NewsArticleOut(BaseModel):
    id: int
    title: str
    author: Optional[str]
    publishedAt: datetime
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    source_name: str
    category: str 
    class Config:
        from_attributes = True
        
class NewsImageOut(BaseModel):
    title: str
    url: str
    urlToImage: str

    class Config:
        from_attributes = True