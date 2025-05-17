from pydantic import BaseModel, HttpUrl

class PostInput(BaseModel):
    title: str
    url: HttpUrl
