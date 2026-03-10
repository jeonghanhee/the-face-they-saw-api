from fastapi import APIRouter
from app.api import auth, scenario, sketch

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(scenario.router, tags=["Scenario"])
api_router.include_router(sketch.router, tags=["Sketch"])