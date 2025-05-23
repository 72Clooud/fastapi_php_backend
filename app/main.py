from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import db
from models.user import User
from models.post import Post
from models.favorites import Favorites
from routes import user, auth, favorites
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST', 'GET'],
    allow_headers=["*"],
)

app.include_router(favorites.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}