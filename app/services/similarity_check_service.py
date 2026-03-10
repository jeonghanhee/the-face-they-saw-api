from fastapi import UploadFile
from app.models import Scenario
from app.utils.prompt_templates import create_similarity_check_user_prompt, SIMILARITY_CHECK_SYSTEM_PROMPT
from app.services.llm_client import generate_content

async def similarity_check(scenario: Scenario, file: UploadFile):
    # gemini-client.py를 통해 유사도 검사하고 유사도를 반환
    sup = create_similarity_check_user_prompt(scenario.composite_sketch.cumulative_description)
    ssp = SIMILARITY_CHECK_SYSTEM_PROMPT
    
    raw_text = await generate_content(sup, ssp, file)
    return raw_text