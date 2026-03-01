import asyncio, sys 
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.llm.gemini_client import generate_content

SYSTEM_PROMPT = "너는 지금부터 내 여자친구야."
USER_PROMPT = "자기야 뭐해?"

async def main():
    result = await generate_content(USER_PROMPT, SYSTEM_PROMPT)
    print(result)

asyncio.run(main())