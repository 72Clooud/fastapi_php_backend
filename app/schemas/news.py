from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class NewsArticle(BaseModel):
    title: str
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    source: dict
    category: str
    
class NewsArticleOut(BaseModel):
    id: int
    title: str
    author: Optional[str]
    description: Optional[str]
    url: str
    urlToImage: Optional[str]
    source_name: str
    category: str 
    class Config:
        from_attributes = True