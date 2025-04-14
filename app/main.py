from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import db
from models.user import User
from routes import user

db.init()

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}