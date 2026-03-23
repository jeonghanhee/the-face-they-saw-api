from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from app.dto import InvestigateRequest, InvestigateResponse
from app.security import secure_endpoint

router = APIRouter()

@router.post("/investigate", response_model=InvestigateResponse, dependencies=[Depends(secure_endpoint)])
async def investigate(req: InvestigateRequest, request: Request, x_language: str = Header(default="ko")):
    return 