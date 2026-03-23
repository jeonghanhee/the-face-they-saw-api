import asyncio, os
from fastapi import UploadFile
from google import genai
from google.genai.types import GenerateContentConfig, Part
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise TypeError("GEMINI_API_KEY not found.")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
if not GEMINI_MODEL_NAME:
    raise TypeError("GEMINI_MODEL_NAME not found.")

client = genai.Client(api_key=GEMINI_API_KEY)

def __generate_content_sync(
    user_prompt: str, 
    system_prompt: str, 
    image_bytes: bytes | None = None, 
    mime_type: str | None = None
) -> str:
    if image_bytes:
        contents = [
            Part.from_bytes(data=image_bytes, mime_type=mime_type),
            user_prompt
        ]
    else:
        contents = user_prompt

    response = client.models.generate_content(
        model=GEMINI_MODEL_NAME,
        contents=contents,
        config=GenerateContentConfig(
            system_instruction=[system_prompt]
        ),
    )
    return response.text

async def generate_content(user_prompt: str, system_prompt: str, image: UploadFile | None = None) -> str:
    image_bytes = None
    mime_type = None

    if image:
        image_bytes = await image.read()
        mime_type = image.content_type

    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, 
        __generate_content_sync,
        user_prompt,
        system_prompt,
        image_bytes,
        mime_type
    )
    return result
