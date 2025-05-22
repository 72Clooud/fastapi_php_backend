from pydantic import BaseModel

class FavoritePost(BaseModel):
    title: str
    url: str
    urlToImage: str

    class Config:
        from_attributes = True