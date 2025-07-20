from fastapi import FastAPI
from app.routers import anime, users

app = FastAPI()

app.include_router(anime.router)
app.include_router(users.router)
