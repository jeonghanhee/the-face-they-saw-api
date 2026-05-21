import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.gemini import generate
from app.prompts.testimony import build_system_prompt, build_user_prompt
from app.schemas.testimony import TestimonyRequest, TestimonyResponse

router = APIRouter()


@router.post("/testimony", response_model=TestimonyResponse)
async def query_witness(req: TestimonyRequest):
    raw = await generate(build_system_prompt(req), build_user_prompt(req.question))
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return JSONResponse(status_code=500, content={"error": "Invalid JSON from LLM", "raw": raw})
