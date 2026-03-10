from fastapi import APIRouter, Header, Request
from fastapi.responses import JSONResponse
from app.dto import GenerateScenarioRequest, GenerateScenarioResponse
from app.services.scenario_service import create_scenario
from app.utils.i18n import get_translation

router = APIRouter()

@router.post("/generate", response_model=GenerateScenarioResponse)
async def generate(req: GenerateScenarioRequest, request: Request, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    manager = request.app.state.manager
    session = await manager.get_session(req.client_id)

    if not session:
        return JSONResponse(status_code=409, content={"message": _("cannot_generate_scenario")})
    if session.scenario:
        return JSONResponse(status_code=409, content={"message": _("already_scenario")})

    new_scenario = await create_scenario(req.level)
    session.set_scenario(new_scenario)
    return {
        "name": new_scenario.witness.name,
        "gender": new_scenario.witness.gender,
        "statement": new_scenario.statement,
        "crime_type": new_scenario.crime_type
    }