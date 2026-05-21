from fastapi import APIRouter, Depends, File, UploadFile

from app.gemini import generate
from app.prompts.portrait import build_user_prompt, system_prompt
from app.schemas.portrait import PortraitItem, PortraitRequest, PortraitResponse

router = APIRouter()


def _parse_response(raw: str) -> tuple[list[PortraitItem], int]:
    detail_block = raw.split("[DETAIL]")[1].split("[TOTAL]")[0].strip()
    total_block = raw.split("[TOTAL]")[1].strip()
    total_score = int(total_block.split("|")[1].replace("%", "").strip())

    details = []
    for line in detail_block.split("\n"):
        parts = line.split("|")
        if len(parts) < 2:
            continue
        name = parts[0].strip()
        value = parts[1].strip()
        score = -1 if value == "판단 불가" else int(value.replace("%", "").strip())
        details.append(PortraitItem(name=name, score=score))

    return details, total_score


@router.post("/portrait", response_model=PortraitResponse)
async def analyze_portrait(
    req: PortraitRequest = Depends(PortraitRequest.as_form),
    file: UploadFile = File(...),
):
    raw = await generate(system_prompt(), build_user_prompt(req.criteria), file)
    details, score = _parse_response(raw)
    return PortraitResponse(details=details, score=score)
