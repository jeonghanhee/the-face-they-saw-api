from fastapi import APIRouter, Depends, File, UploadFile
from app.dto import UploadRequest, UploadResponse
from app.llm_client import generate_content
from app.prompt_templates import SIMILARITY_CHECK_SYSTEM_PROMPT
from app.prompt_parser import create_similarity_check_user_prompt
from app.security import secure_endpoint

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload(req: UploadRequest = Depends(UploadRequest.as_form), file: UploadFile = File(...), dependencies=[Depends(secure_endpoint)]):
    sup = create_similarity_check_user_prompt(req.description)
    result = await generate_content(sup, SIMILARITY_CHECK_SYSTEM_PROMPT, file)
    
    detail_section = result.split("[DETAIL]")[1].split("[TOTAL]")[0].strip()
    total_section = result.split("[TOTAL]")[1].strip()

    detail_lines = detail_section.split("\n")
    total_score = total_section.split("|")[1].replace("%", "")

    details = [
        (line.split("|")[0], int(line.split("|")[1].replace("%", "")), float(line.split("|")[2])) 
        for line in detail_lines
    ]

    return {
        "details": details,
        "score": total_score
    }