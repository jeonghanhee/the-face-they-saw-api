from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from app.schemas import *
from app.middleware.security import secure_endpoint

app = FastAPI(title="The Face They Saw API")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

clients = set([])

@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/join", status_code=200, response_model=JoinResponse, dependencies=secure_endpoint())
def join(req: JoinRequest):
    if req.client_id in clients:
        return JSONResponse(
            status_code=409,
            content={
                "message": "이미 대기열에 등록된 클라이언트입니다."
            }
        )
    clients.add(req.client_id)
    return {
        "message": "대기열에 성공적으로 등록했습니다."
    }