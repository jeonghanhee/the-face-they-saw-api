import json

from fastapi import APIRouter, Depends, Header, Request
from fastapi.responses import JSONResponse
from app.dto import InvestigateRequest, InvestigateResponse
from app.llm_client import generate_content
from app.prompt_parser import create_investigate_system_prompt, create_investigate_user_prompt
from app.security import secure_gate

router = APIRouter()

@router.post("/investigate", response_model=InvestigateResponse, dependencies=[Depends(secure_gate)])
async def investigate(req: InvestigateRequest):
    sup = create_investigate_system_prompt(req.case_name, req.name, req.reliability, req.memory, req.personality)
    result = await generate_content(sup, create_investigate_user_prompt(req.question))

    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        return JSONResponse(status_code=500, content={"error": "Invalid JSON from LLM", "raw": result})

    return parsed