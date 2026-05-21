from fastapi import APIRouter
from app.routers import health, testimony, portrait

router = APIRouter()
router.include_router(health.router, tags=["Health"])
router.include_router(testimony.router, tags=["Testimony"])
router.include_router(portrait.router, tags=["Portrait"])
