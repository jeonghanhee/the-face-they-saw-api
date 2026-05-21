import asyncio, os
from fastapi import UploadFile
from google import genai
from google.genai.types import GenerateContentConfig, Part
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("GEMINI_API_KEY")
if not _API_KEY:
    raise EnvironmentError("GEMINI_API_KEY not set")

_MODEL = os.getenv("GEMINI_MODEL_NAME")
if not _MODEL:
    raise EnvironmentError("GEMINI_MODEL_NAME not set")

_client = genai.Client(api_key=_API_KEY)


def _call_sync(
    system_prompt: str,
    user_prompt: str,
    image_bytes: bytes | None = None,
    mime_type: str | None = None,
) -> str:
    contents = (
        [Part.from_bytes(data=image_bytes, mime_type=mime_type), user_prompt]
        if image_bytes
        else user_prompt
    )
    response = _client.models.generate_content(
        model=_MODEL,
        contents=contents,
        config=GenerateContentConfig(system_instruction=[system_prompt]),
    )
    return response.text


async def generate(
    system_prompt: str,
    user_prompt: str,
    image: UploadFile | None = None,
) -> str:
    image_bytes = await image.read() if image else None
    mime_type = image.content_type if image else None
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, _call_sync, system_prompt, user_prompt, image_bytes, mime_type
    )
