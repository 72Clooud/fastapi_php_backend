from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import db
from models.user import User
from models.favorites import Favorites
from routes import user, auth, favorites, news
from contextlib import asynccontextmanager
from services.news import news_api_handler

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    async with db.get_session() as session:
        await news_api_handler.load_news_to_db_concurrent(session)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)

app.include_router(favorites.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(news.router)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}