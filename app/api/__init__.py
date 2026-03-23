from fastapi import APIRouter
from . import investigate, ping, upload

api_router = APIRouter()

api_router.include_router(ping.router, tags=["Ping"])
api_router.include_router(investigate.router, tags=["Investigate"])
api_router.include_router(upload.router, tags=["Upload"])