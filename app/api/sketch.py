from fastapi import APIRouter, Depends, File, Header, UploadFile, Request
from fastapi.responses import JSONResponse
from app.dto import GeneralRequest, UploadMontageResponse
from app.services.similarity_check_service import similarity_check
from app.utils.i18n import get_translation

router = APIRouter()

@router.post("/upload", response_model=UploadMontageResponse)
async def upload(
    request: Request,
    req: GeneralRequest = Depends(GeneralRequest.as_form), 
    file: UploadFile = File(...), 
    x_language: str = Header(default="ko")
):
    _ = get_translation(x_language)
    manager = request.app.state.manager
    session = await manager.get_session(req.client_id)

    if not session or not session.scenario:
        return JSONResponse(status_code=409, content={"message": _("not_found_scenario")})
    
    result = await similarity_check(session.scenario, file)
    
    detail_section = result.split("[DETAIL]")[1].split("[TOTAL]")[0].strip()
    total_section = result.split("[TOTAL]")[1].strip()

    detail_lines = detail_section.split("\n")
    total_score = total_section.split("|")[1].replace("%", "")

    details = [
        (line.split("|")[0], int(line.split("|")[1].replace("%", "")), float(line.split("|")[2])) 
        for line in detail_lines
    ]

    session.clear()

    return {
        "details": details,
        "total_score": total_score
    }