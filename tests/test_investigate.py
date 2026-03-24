import time
import hashlib
import requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
SIGN_SECRET = "tfts-game-key-v1"
GAME_KEY = "tfts-sign-secret"

def make_headers():
    timestamp = int(time.time())
    raw = f"{SIGN_SECRET}{timestamp}"
    signature = hashlib.sha256(raw.encode()).hexdigest()

    return {
        "X-Game-Key": GAME_KEY,
        "X-Timestamp": str(timestamp),
        "X-Signature": signature
    }


def test():
    headers = make_headers()

    payload = {
        "criteria": """- 동그란 얼굴형
- 찢어진 눈매와 긴 코
- 일자의 입매
"""
    }

    image_path = Path(__file__).parent / "sample1.jpg"

    with open(image_path, "rb") as f:
        files = {
            "file": ("sample1.jpg", f, "image/jpeg")
        }

        response = requests.post(
            f"{BASE_URL}/api/upload",
            data=payload,
            files=files,
            headers=headers
        )

    print("status:", response.status_code)
    print("response:", response.json())

test()