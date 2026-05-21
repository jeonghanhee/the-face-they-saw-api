import time, hashlib, requests
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
SIGN_SECRET = "tfts-game-key-v1"
GAME_KEY = "tfts-sign-secret"


def _make_headers() -> dict:
    timestamp = int(time.time())
    signature = hashlib.sha256(f"{SIGN_SECRET}{timestamp}".encode()).hexdigest()
    return {
        "X-Game-Key": GAME_KEY,
        "X-Timestamp": str(timestamp),
        "X-Signature": signature,
    }


def test_analyze_portrait():
    headers = _make_headers()
    payload = {
        "criteria": "- 동그란 얼굴형\n- 찢어진 눈매와 긴 코\n- 일자의 입매"
    }
    image_path = Path(__file__).parent / "sample1.jpg"

    with open(image_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/portrait",
            data=payload,
            files={"file": ("sample1.jpg", f, "image/jpeg")},
            headers=headers,
        )

    print("status:", response.status_code)
    print("response:", response.json())


test_analyze_portrait()
