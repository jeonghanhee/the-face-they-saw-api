from fastapi import Depends, FastAPI, File, Header, UploadFile
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.services.scenario_factory import create_scenario
from app.services.similarity_service import similarity_check
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

@app.post("/join_game", status_code=200, response_model=GeneralResponse, dependencies=secure_endpoint())
async def join_game(req: GeneralRequest, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    exists = await cda.get_client(req.client_id)
    if exists:
        return JSONResponse(status_code=409, content={"message": _("already_registered")})
    await cda.add_client(req.client_id)
    return {"message": _("register_success")}

@app.post("/leave_game", status_code=200, response_model=GeneralResponse, dependencies=secure_endpoint())
async def leave_game(req: GeneralRequest, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    exists = await cda.get_client(req.client_id)
    if exists:
        await cda.remove_client(req.client_id)
        return {"message": _("removed_success")}
    return JSONResponse(status_code=409, content={"message": _("not_registered")})

@app.post("/retrieve_scenario", status_code=200, response_model=RetrieveScenarioResponse)
async def retrieve_scenario(req: RetrieveScenarioRequest, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    exists = await cda.get_client(req.client_id)
    if not exists:
        return JSONResponse(status_code=409, content={"message": _("cannot_retrieve_scenario")})
    if exists.scenario:
        return JSONResponse(status_code=409, content={"message": _("alreay_scenario")})
    new_scenario = await create_scenario(req.level)
    exists.set_scenario(new_scenario) # 시나리오 등록
    return {
        "name": new_scenario.witness.name,
        "gender": new_scenario.witness.gender,
        "statement": new_scenario.statement,
        "crime_type": new_scenario.crime_type
    }

@app.post("/upload_montage", status_code=200, response_model=UploadMontageResponse)
async def upload_montage(req: GeneralRequest = Depends(GeneralRequest.as_form), file: UploadFile = File(), x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    exists = await cda.get_client(req.client_id) 
    if not exists:
        return JSONResponse(status_code=409, content={"message": _("not_registered")})
    if not exists.scenario:
        return JSONResponse(status_code=409, content={"message": _("not_found_scenario")})
    
    result = await similarity_check(exists.scenario, file)
    
    detail_section = result.split("[DETAIL]")[1].split("[TOTAL]")[0].strip()
    total_section = result.split("[TOTAL]")[1].strip()

    detail_lines = detail_section.split("\n")
    total_score = total_section.split("|")[1].replace("%", "")

    details = [
        (line.split("|")[0], int(line.split("|")[1].replace("%", "")), float(line.split("|")[2])) 
        for line in detail_lines
    ]

    exists.set_scenario(None) # 시나리오 제거 

    return {
        "details": details,
        "total_score": total_score
    }