from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from app.dto import GeneralRequest, GeneralResponse
from app.core.security import secure_endpoint
from app.utils.i18n import get_translation

router = APIRouter()

@router.post("/join", response_model=GeneralResponse, dependencies=[Depends(secure_endpoint)])
async def join_game(req: GeneralRequest, request: Request, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    manager = request.app.state.manager
    if await manager.get_session(req.client_id):
        return JSONResponse(status_code=409, content={"message": _("already_registered")})
    await manager.add_session(req.client_id)
    return {"message": _("register_success")}

@router.post("/leave", response_model=GeneralResponse, dependencies=[Depends(secure_endpoint)])
async def leave_game(req: GeneralRequest, request: Request, x_language: str = Header(default="ko")):
    _ = get_translation(x_language)
    manager = request.app.state.manager
    if await manager.remove_session(req.client_id):
        return {"message": _("removed_success")}
    return JSONResponse(status_code=409, content={"message": _("not_registered")})