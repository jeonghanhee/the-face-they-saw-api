from fastapi import APIRouter, Depends
from app.security import secure_gate

router = APIRouter()

@router.get("/ping", dependencies=[Depends(secure_gate)])
async def ping():
    return {"status": "ok"}