from fastapi import FastAPI
from app.routers import router

app = FastAPI(title="The Face They Saw API")
app.include_router(router, prefix="/api")
