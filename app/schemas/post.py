from pydantic import BaseModel, HttpUrl

class PostInput(BaseModel):
    id: int
