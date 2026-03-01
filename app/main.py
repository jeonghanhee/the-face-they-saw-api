from fastapi import FastAPI, Header, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.schemas import *
from app.middleware.security import secure_endpoint
from app.cda import CDA
from babel.support import Translations
from pathlib import Path

app = FastAPI(title="The Face They Saw API")
cda = CDA()

LOCALES_DIR = Path(__file__).parent / "locales"

translations_cache = {
    "ko": Translations.load(LOCALES_DIR, locales=["ko_KR"]),
    "en": Translations.load(LOCALES_DIR, locales=["en_US"]),
}

def get_translation(lang: str):
    return translations_cache.get(lang.lower(), translations_cache["ko"]).gettext

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.post("/join_game", status_code=200, response_model=JoinResponse, dependencies=secure_endpoint())
async def join_game(req: JoinRequest, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    exists = await cda.get_client(req.client_id)
    if exists:
        return JSONResponse(status_code=409, content={"message": _("already_registered")})
    await cda.add_client(req.client_id)
    return {"message": _("register_success")}

@app.post("/leave_game", status_code=200, response_model=LeaveResponse, dependencies=secure_endpoint())
async def leave_game(req: LeaveRequest, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    exists = await cda.get_client(req.client_id)
    if exists:
        await cda.remove_client(req.client_id)
        return {"message": _("removed_success")}
    return JSONResponse(status_code=409, content={"message": _("not_registered")})