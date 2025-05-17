from pydantic import BaseModel

class FavoritePost(BaseModel):
    title: str
    url: str

    class Config:
        from_attributes = True