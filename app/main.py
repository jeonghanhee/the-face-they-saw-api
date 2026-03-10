from fastapi import FastAPI
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.api import api_router
from app.core.session_manager import SessionManager

app = FastAPI(title="The Face They Saw API")

app.state.manager = SessionManager()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(api_router, prefix="/api")

@app.get("/ping")
async def ping():
    return {"status": "ok"}