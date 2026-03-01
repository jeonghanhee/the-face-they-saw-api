import asyncio, os
from google import genai
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise TypeError("GEMINI_API_KEY not found.")

client = genai.Client(api_key=GEMINI_API_KEY)

def __generate_content_sync(user_prompt: str, system_prompt: str) -> str:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=GenerateContentConfig(
            system_instruction=[system_prompt]
        ),
    )
    return response.text

async def generate_content(user_prompt: str, system_prompt: str) -> str:
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, 
        __generate_content_sync,
        user_prompt,
        system_prompt
    )
    return result
