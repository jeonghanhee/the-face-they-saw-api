from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.schemas import *
from app.middleware.security import secure_endpoint
from app.cda import CDA

app = FastAPI(title="The Face They Saw API")
cda = CDA()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.get("/ping")
async def ping():
    return {"status": "ok"}

@app.post("/join_game", status_code=200, response_model=JoinResponse, dependencies=secure_endpoint())
async def join_game(req: JoinRequest):
    exists = await cda.get_client(req.client_id)
    if exists:
        return JSONResponse(
            status_code=409,
            content={"message": "이미 대기열에 등록된 클라이언트입니다."}
        )
    await cda.add_client(req.client_id)
    return {"message": "대기열에 성공적으로 등록했습니다."}

@app.post("/leave_game", status_code=200, response_model=LeaveResponse, dependencies=secure_endpoint())
async def leave_game(req: LeaveRequest):
    exists = await cda.get_client(req.client_id)
    print(exists)
    if exists:
        await cda.remove_client(req.client_id)
        return {"message": "성공적으로 대기열에서 제거되었습니다."}
    return JSONResponse(
        status_code=409,
        content={"message": "대기열에 등록되어있는 상태가 아닙니다."}
    )
